from pathlib import Path
from uuid import UUID
import json

from datasets import Dataset
from sqlalchemy.orm import Session

from services.data_preparation.app.models.prepared_artifact import (
    PreparedArtifact,
)
from services.run_orchestrator.app.models.training_run import (
    TrainingRunStatus,
)
from services.run_orchestrator.app.repositories.training_run_repository import (
    TrainingRunRepository,
)
from services.run_orchestrator.app.services.artifact_loader import (
    load_manifest,
    load_training_records,
)

from services.dataset_registry.app.storage.minio_client import (
    upload_bytes,
    upload_directory_as_zip,
)

from packages.finetuning.dataset_adapter import records_to_text
from packages.finetuning.manifest import build_run_manifest
from packages.finetuning.model_loader import (
    load_base_model,
    load_tokenizer,
)
from packages.finetuning.trainer import (
    apply_lora,
    create_trainer,
    prepare_training_arguments,
    save_adapter,
)


class TrainingWorker:

    def __init__(self):
        self.repository = TrainingRunRepository()

    def run_once(
        self,
        db: Session,
        run_id: UUID,
    ):
        run = self.repository.get_by_id(
            db=db,
            run_id=run_id,
        )

        if run is None:
            raise ValueError("Training run not found.")

        if run.status != TrainingRunStatus.QUEUED.value:
            raise ValueError(
                f"Training run is {run.status}."
            )

        try:
            config = run.config or {}
            adaptation = config.get("adaptation", {})
            training = config.get("training", {})

            method = str(
                adaptation.get("method", "lora")
            ).lower()

            if method != "lora":
                raise ValueError(
                    "MVP currently executes LoRA training only."
                )

            artifact = (
                db.query(PreparedArtifact)
                .filter(
                    PreparedArtifact.id == run.prepared_artifact_id
                )
                .first()
            )

            if artifact is None:
                raise ValueError(
                    "Prepared artifact not found."
                )

            records = load_training_records(
                db=db,
                prepared_artifact=artifact,
            )

            if not records:
                raise ValueError(
                    "Training dataset is empty."
                )

            prepared_manifest = load_manifest(artifact)

            texts = records_to_text(records)

            if not texts:
                raise ValueError(
                    "No training text could be created."
                )

            tokenizer = load_tokenizer(run.base_model)

            model = load_base_model(
                run.base_model,
                quantized=False,
            )

            model = apply_lora(
                model=model,
                config=adaptation,
            )

            tokenized = tokenizer(
                texts,
                truncation=True,
                padding="max_length",
                max_length=int(
                    training.get("max_length", 512)
                ),
            )

            train_dataset = Dataset.from_dict(tokenized)

            def add_labels(batch):
                labels = []

                for input_ids, attention_mask in zip(
                    batch["input_ids"],
                    batch["attention_mask"],
                ):
                    labels.append([
                        token_id if mask == 1 else -100
                        for token_id, mask in zip(
                            input_ids,
                            attention_mask,
                        )
                    ])

                return {"labels": labels}

            train_dataset = train_dataset.map(
                add_labels,
                batched=True,
            )

            output_dir = (
                Path("training_outputs")
                / str(run.id)
            )

            output_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            batch_size = int(
                training.get("batch_size", 1)
            )
            epochs = int(
                training.get("epochs", 1)
            )

            steps_per_epoch = max(
                1,
                (len(train_dataset) + batch_size - 1)
                // batch_size,
            )

            total_steps = steps_per_epoch * epochs

            training_args = prepare_training_arguments(
                output_dir=str(output_dir),
                learning_rate=float(
                    training.get("learning_rate", 0.0002)
                ),
                epochs=epochs,
                batch_size=batch_size,
                seed=int(
                    training.get("seed", 42)
                ),
                save_steps=int(
                    training.get("save_steps", 100)
                ),
                logging_steps=int(
                    training.get("logging_steps", 10)
                ),
            )

            trainer = create_trainer(
                model=model,
                tokenizer=tokenizer,
                train_dataset=train_dataset,
                training_args=training_args,
            )

            self.repository.mark_running(
                db=db,
                run=run,
                total_steps=total_steps,
            )

            train_result = trainer.train()

            adapter_dir = output_dir / "adapter"

            save_adapter(
                model=model,
                output_dir=str(adapter_dir),
            )

            metrics = {}

            if getattr(train_result, "metrics", None):
                for key, value in train_result.metrics.items():
                    if isinstance(value, (int, float)):
                        metrics[key] = float(value)

            metrics["records"] = len(records)
            metrics["training_steps"] = int(
                getattr(
                    trainer.state,
                    "global_step",
                    total_steps,
                )
            )
            metrics["prepared_manifest_loaded"] = bool(
                prepared_manifest
            )

            adapter_key = (
                f"training/{run.id}/adapter.zip"
            )

            upload_directory_as_zip(
                directory=adapter_dir,
                object_key=adapter_key,
            )

            manifest_data = build_run_manifest(
                run_id=str(run.id),
                dataset_id=str(run.dataset_id),
                prepared_artifact_id=str(
                    run.prepared_artifact_id
                ),
                dataset_version=config.get(
                    "dataset_version",
                    "unknown",
                ),
                base_model=run.base_model,
                adaptation=adaptation,
                training=training,
                compute=config.get("compute", {}),
                evaluation_plan=config.get(
                    "evaluation_plan",
                    {},
                ),
                tokenizer=run.base_model,
                seed=int(
                    training.get("seed", 42)
                ),
                extra={
                    "training_records": len(records),
                    "prepared_manifest": prepared_manifest,
                    "final_metrics": metrics,
                },
            )

            manifest_key = (
                f"training/{run.id}/manifest.json"
            )

            manifest_bytes = json.dumps(
                manifest_data,
                indent=2,
                ensure_ascii=False,
            ).encode("utf-8")

            upload_bytes(
                data=manifest_bytes,
                object_key=manifest_key,
                content_type="application/json",
            )

            return self.repository.mark_completed(
                db=db,
                run=run,
                adapter_object_key=adapter_key,
                manifest_object_key=manifest_key,
                metrics=metrics,
            )

        except Exception as exc:
            self.repository.mark_failed(
                db=db,
                run=run,
                error_message=str(exc),
            )
            raise