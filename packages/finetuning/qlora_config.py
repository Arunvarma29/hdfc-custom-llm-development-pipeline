from dataclasses import dataclass
from typing import Any

from packages.finetuning.lora_config import LoRAConfig


@dataclass(frozen=True)
class QLoRAConfig(LoRAConfig):
    bits: int = 4
    double_quant: bool = True
    quant_type: str = "nf4"

    def validate(self) -> None:
        super().validate()

        if self.bits not in {4, 8}:
            raise ValueError(
                "QLoRA bits must be 4 or 8."
            )

        if self.quant_type not in {"nf4", "fp4"}:
            raise ValueError(
                "QLoRA quant_type must be nf4 or fp4."
            )

    def to_dict(self) -> dict[str, Any]:
        self.validate()

        data = super().to_dict()

        data.update(
            {
                "method": "qlora",
                "bits": self.bits,
                "double_quant": self.double_quant,
                "quant_type": self.quant_type,
            }
        )

        return data