from typing import Any


def load_tokenizer(
    model_name_or_path: str,
):
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path,
        use_fast=True,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = (
            tokenizer.eos_token
        )

    return tokenizer


def load_base_model(
    model_name_or_path: str,
    *,
    quantized: bool = False,
) -> Any:
    from transformers import AutoModelForCausalLM

    kwargs: dict[str, Any] = {}

    if quantized:
        from transformers import (
            BitsAndBytesConfig,
        )

        kwargs[
            "quantization_config"
        ] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype="float16",
        )

    return AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        **kwargs,
    )