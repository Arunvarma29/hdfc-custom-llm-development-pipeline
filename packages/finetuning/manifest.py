from datetime import UTC, datetime
from typing import Any


def build_run_manifest(
    *,
    run_id: str,
    dataset_id: str,
    prepared_artifact_id: str,
    dataset_version: str,
    base_model: str,
    adaptation: dict,
    training: dict,
    compute: dict,
    evaluation_plan: dict,
    tokenizer: str,
    seed: int = 42,
    code_commit: str | None = None,
    container_digest: str | None = None,
    extra: dict[str, Any] | None = None,
):
    manifest = {
        "run_id": run_id,
        "dataset_id": dataset_id,
        "prepared_artifact_id": (
            prepared_artifact_id
        ),
        "dataset_version": dataset_version,
        "base_model": base_model,
        "adaptation": adaptation,
        "training": training,
        "compute": compute,
        "evaluation_plan": evaluation_plan,
        "reproducibility": {
            "tokenizer": tokenizer,
            "seed": seed,
            "code_commit": code_commit,
            "container_digest": container_digest,
        },
        "created_at": (
            datetime.now(UTC).isoformat()
        ),
    }

    if extra:
        manifest["extra"] = extra

    return manifest