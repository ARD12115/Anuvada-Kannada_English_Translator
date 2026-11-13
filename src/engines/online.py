from threading import RLock
from time import sleep

from src.models import Lang
from src.utils.errors import EngineUnavailableError

REQUEST_TIMEOUT = (3.05, 10.0)
_REQUEST_PATCH_LOCK = RLock()


class _RequestsWithTimeout:
    def __init__(self, requests_module, timeout: tuple[float, float]):
        self._requests = requests_module
        self._timeout = timeout

    def get(self, *args, **kwargs):
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = self._timeout
        return self._requests.get(*args, **kwargs)


def _translate_with_timeout(translator, text: str) -> str:
    import deep_translator.google as google_module

    # deep-translator 1.11.4 calls requests.get without a timeout parameter.
    with _REQUEST_PATCH_LOCK:
        original_requests = google_module.requests
        google_module.requests = _RequestsWithTimeout(
            original_requests, REQUEST_TIMEOUT
        )
        try:
            return translator.translate(text)
        finally:
            google_module.requests = original_requests


class OnlineEngine:
    name = "online"
    max_chunk_length = 4500

    def __init__(self, translator_factory=None, retries: int = 1):
        self._translator_factory = translator_factory
        self.retries = retries

    def available(self) -> bool:
        try:
            from deep_translator import GoogleTranslator  # noqa: F401
        except ImportError:
            return False
        return True

    def _factory(self):
        if self._translator_factory is not None:
            return self._translator_factory
        try:
            from deep_translator import GoogleTranslator
        except ImportError as exc:
            raise EngineUnavailableError(
                "Online translation dependency is not installed."
            ) from exc
        return GoogleTranslator

    @staticmethod
    def _chunks(text: str, limit: int) -> list[str]:
        chunks = []
        remaining = text
        while len(remaining) > limit:
            split_at = remaining.rfind(" ", 0, limit + 1)
            if split_at <= 0:
                split_at = limit
            chunks.append(remaining[:split_at])
            remaining = remaining[split_at:].lstrip()
        if remaining:
            chunks.append(remaining)
        return chunks

    def translate(self, text: str, src: Lang, tgt: Lang) -> str:
        if not text.strip():
            return text
        factory = self._factory()
        results = []
        for chunk in self._chunks(text, self.max_chunk_length):
            last_error = None
            for attempt in range(self.retries + 1):
                try:
                    translator = factory(source=src, target=tgt)
                    result = _translate_with_timeout(translator, chunk)
                    if not result:
                        raise ValueError("Translation provider returned no text.")
                    results.append(result)
                    last_error = None
                    break
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    if attempt < self.retries:
                        sleep(0.2)
            if last_error is not None:
                raise EngineUnavailableError(
                    "Online translation failed. Check your connection or choose Offline."
                ) from last_error
        return " ".join(results)
