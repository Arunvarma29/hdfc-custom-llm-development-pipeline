from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LoRAConfig:
    rank: int = 16
    alpha: int = 32
    dropout: float = 0.05
    target_modules: tuple[str, ...] = (
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
    )
    bias: str = "none"
    task_type: str = "CAUSAL_LM"

    def validate(self) -> None:
        if self.rank <= 0:
            raise ValueError("LoRA rank must be greater than 0.")

        if self.alpha <= 0:
            raise ValueError("LoRA alpha must be greater than 0.")

        if not 0.0 <= self.dropout <= 1.0:
            raise ValueError(
                "LoRA dropout must be between 0 and 1."
            )

        if not self.target_modules:
            raise ValueError(
                "At least one target module is required."
            )

        if self.bias not in {"none", "all", "lora_only"}:
            raise ValueError(
                "LoRA bias must be none, all, or lora_only."
            )

        if self.task_type != "CAUSAL_LM":
            raise ValueError(
                "This MVP supports CAUSAL_LM only."
            )

    def to_dict(self) -> dict[str, Any]:
        self.validate()

        return {
            "method": "lora",
            "rank": self.rank,
            "alpha": self.alpha,
            "dropout": self.dropout,
            "target_modules": list(self.target_modules),
            "bias": self.bias,
            "task_type": self.task_type,
        }