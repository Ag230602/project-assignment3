from __future__ import annotations

from pathlib import Path

from .config import DEFAULT_MODEL, LOCAL_BASE_MODEL_PATH, MODEL_DIR


class ModelService:
    def __init__(self):
        self._tokenizer = None
        self._model = None
        self._load_error = None

    @property
    def ready(self) -> bool:
        self._ensure_loaded()
        return self._model is not None and self._tokenizer is not None

    @property
    def load_error(self):
        self._ensure_loaded()
        return self._load_error

    def _ensure_loaded(self):
        if self._tokenizer is not None or self._load_error is not None:
            return

        try:
            base_model_source = self._resolve_base_model_source()
            if base_model_source is None:
                raise FileNotFoundError(
                    "No local base model was found. Set LOCAL_BASE_MODEL_PATH to a downloaded model."
                )

            import torch
            from peft import PeftModel
            from transformers import AutoModelForCausalLM, AutoTokenizer

            tokenizer_source = MODEL_DIR if Path(MODEL_DIR).exists() else DEFAULT_MODEL
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_source, local_files_only=True)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token

            base_model = AutoModelForCausalLM.from_pretrained(
                base_model_source,
                local_files_only=True,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
            )
            if Path(MODEL_DIR).exists():
                model = PeftModel.from_pretrained(base_model, MODEL_DIR)
            else:
                model = base_model
            model.eval()

            self._tokenizer = tokenizer
            self._model = model
        except Exception as exc:
            self._load_error = exc

    def _resolve_base_model_source(self):
        if LOCAL_BASE_MODEL_PATH and Path(LOCAL_BASE_MODEL_PATH).exists():
            return LOCAL_BASE_MODEL_PATH
        if Path(DEFAULT_MODEL).exists():
            return DEFAULT_MODEL
        return None

    def generate(self, prompt: str, max_new_tokens: int = 140) -> tuple[str, bool]:
        self._ensure_loaded()
        if self._model is None or self._tokenizer is None:
            return self._fallback_response(prompt), True

        import torch

        tokens = self._tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            device = next(self._model.parameters()).device
            tokens = {key: value.to(device) for key, value in tokens.items()}
            output = self._model.generate(
                **tokens,
                max_new_tokens=max_new_tokens,
                do_sample=False,
            )

        decoded = self._tokenizer.decode(output[0], skip_special_tokens=True)
        answer = decoded.split("Response:", 1)[-1].strip() if "Response:" in decoded else decoded
        return answer, False

    def _fallback_response(self, prompt: str) -> str:
        condensed = " ".join(prompt.split())
        return (
            "Fallback response: the domain-adapted model is not loaded, so this answer is "
            "based on retrieved context and warehouse facts. "
            f"Prompt summary: {condensed[:280]}"
        )
