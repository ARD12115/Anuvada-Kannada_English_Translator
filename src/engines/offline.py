from functools import lru_cache

from src.models import Lang
from src.utils.errors import EngineUnavailableError
from src.utils.text import split_sentences

_MODEL_CODES = {"kn": "kan_Knda", "en": "eng_Latn"}


class OfflineEngine:
    name = "offline"

    def __init__(self, model_name: str = "facebook/nllb-200-distilled-600M", loader=None):
        self.model_name = model_name
        self._loader = loader

    def available(self) -> bool:
        try:
            import transformers  # noqa: F401
            import torch  # noqa: F401
        except ImportError:
            return False
        return True

    @lru_cache(maxsize=1)
    def _load(self):
        if self._loader is not None:
            return self._loader(self.model_name)
        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
            import torch
        except ImportError as exc:
            raise EngineUnavailableError("Offline translation dependencies are not installed.") from exc
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        except Exception as exc:
            raise EngineUnavailableError(
                "The offline model could not be loaded. Download it during setup or use Online."
            ) from exc
        model.eval()
        return tokenizer, model, torch

    def translate(self, text: str, src: Lang, tgt: Lang) -> str:
        if not text.strip():
            return text
        tokenizer, model, torch = self._load()
        tokenizer.src_lang = _MODEL_CODES[src]
        sentences = split_sentences(text) or [text]
        output = []
        for start in range(0, len(sentences), 8):
            batch = sentences[start : start + 8]
            try:
                encoded = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=512)
                with torch.no_grad():
                    generated = model.generate(
                        **encoded,
                        forced_bos_token_id=tokenizer.convert_tokens_to_ids(_MODEL_CODES[tgt]),
                        max_length=512,
                    )
                output.extend(tokenizer.batch_decode(generated, skip_special_tokens=True))
            except Exception as exc:
                raise EngineUnavailableError("Offline translation failed for this text.") from exc
        return " ".join(output)
