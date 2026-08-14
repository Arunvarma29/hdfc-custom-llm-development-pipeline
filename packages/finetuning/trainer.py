from typing import Any


def apply_lora(
    model: Any,
    config: dict,
):
    from peft import (
        LoraConfig,
        TaskType,
        get_peft_model,
    )

    peft_config = LoraConfig(
        r=int(config["rank"]),
        lora_alpha=int(config["alpha"]),
        lora_dropout=float(
            config["dropout"]
        ),
        target_modules=config[
            "target_modules"
        ],
        bias=config.get(
            "bias",
            "none",
        ),
        task_type=TaskType.CAUSAL_LM,
    )

    model = get_peft_model(
        model,
        peft_config,
    )

    return model


def prepare_training_arguments(
    *,
    output_dir: str,
    learning_rate: float,
    epochs: int,
    batch_size: int,
    seed: int,
    save_steps: int = 100,
    logging_steps: int = 10,
):
    from transformers import TrainingArguments

    return TrainingArguments(
        output_dir=output_dir,
        learning_rate=learning_rate,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        save_steps=save_steps,
        logging_steps=logging_steps,
        seed=seed,
        report_to="none",
        remove_unused_columns=False,
    )


def create_trainer(
    *,
    model: Any,
    tokenizer: Any,
    train_dataset: Any,
    training_args: Any,
):
    from transformers import Trainer

    return Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer,
    )


def save_adapter(
    model: Any,
    output_dir: str,
):
    model.save_pretrained(
        output_dir
    )

    return output_dir