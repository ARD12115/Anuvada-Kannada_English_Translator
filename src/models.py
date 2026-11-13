from dataclasses import dataclass
from typing import Literal

Lang = Literal["kn", "en"]


@dataclass(frozen=True)
class TranslationResult:
    text: str
    source_lang: Lang
    target_lang: Lang
    engine: str
    fell_back: bool = False
