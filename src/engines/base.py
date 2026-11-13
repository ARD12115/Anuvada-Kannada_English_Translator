from typing import Protocol

from src.models import Lang


class TranslationEngine(Protocol):
    name: str

    def translate(self, text: str, src: Lang, tgt: Lang) -> str: ...

    def available(self) -> bool: ...
