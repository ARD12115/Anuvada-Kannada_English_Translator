from threading import RLock

from src.models import Lang
from src.utils.errors import EngineUnavailableError
from src.utils.text import split_sentences

_MODEL_CODES = {"kn": "kan_Knda", "en": "eng_Latn"}


class OfflineEngine:
    name = "offline"

    def __init__(
        self, model_name: str = "facebook/nllb-200-distilled-600M", loader=None
    ):
        self.model_name = model_name
        self._loader = loader
        self._resources = None
        self._lock = RLock()

    def available(self) -> bool:
        try:
            import torch  # noqa: F401
            import transformers  # noqa: F401
        except ImportError:
            return False
        return True

    def _load(self):
        with self._lock:
            if self._resources is not None:
                return self._resources
            if self._loader is not None:
                self._resources = self._loader(self.model_name)
                return self._resources
            try:
                import torch
                from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
            except ImportError as exc:
                raise EngineUnavailableError(
                    "Offline translation dependencies are not installed."
                ) from exc
            try:
                tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name, local_files_only=True
                )
                model = AutoModelForSeq2SeqLM.from_pretrained(
                    self.model_name, local_files_only=True
                )
            except Exception as exc:
                raise EngineUnavailableError(
                    "The offline model could not be loaded. Download it during setup or use Online."
                ) from exc
            model.eval()
            self._resources = (tokenizer, model, torch)
            return self._resources

    def translate(self, text: str, src: Lang, tgt: Lang) -> str:
        if not text.strip():
            return text
        with self._lock:
            tokenizer, model, torch = self._load()
            tokenizer.src_lang = _MODEL_CODES[src]
            output = []
            for sentence in split_sentences(text) or [text]:
                try:
                    encoded = tokenizer(
                        sentence,
                        return_tensors="pt",
                        padding=True,
                        truncation=True,
                        max_length=512,
                        return_overflowing_tokens=True,
                        stride=0,
                    )
                    input_ids = encoded["input_ids"]
                    attention_mask = encoded.get("attention_mask")
                    for start in range(0, len(input_ids), 8):
                        end = start + 8
                        model_inputs = {"input_ids": input_ids[start:end]}
                        if attention_mask is not None:
                            model_inputs["attention_mask"] = attention_mask[start:end]
                        with torch.no_grad():
                            generated = model.generate(
                                **model_inputs,
                                forced_bos_token_id=tokenizer.convert_tokens_to_ids(
                                    _MODEL_CODES[tgt]
                                ),
                                max_length=512,
                            )
                        output.extend(
                            tokenizer.batch_decode(generated, skip_special_tokens=True)
                        )
                except Exception as exc:
                    raise EngineUnavailableError(
                        "Offline translation failed for this text."
                    ) from exc
            return " ".join(output)
