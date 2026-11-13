import logging

from src.engines.base import TranslationEngine
from src.engines.offline import OfflineEngine
from src.engines.online import OnlineEngine
from src.glossary import apply_post, apply_pre
from src.models import Lang, TranslationResult
from src.utils.errors import EmptyInputError, EngineUnavailableError
from src.utils.lang import detect
from src.utils.text import translate_preserving_lines

logger = logging.getLogger(__name__)


def translate(
    text: str,
    preferred: str = "online",
    source_lang: Lang | None = None,
    target_lang: Lang | None = None,
    engines: dict[str, TranslationEngine] | None = None,
) -> TranslationResult:
    if not text.strip():
        raise EmptyInputError("Enter text to translate.")
    source = source_lang or detect(text)
    target = target_lang or ("en" if source == "kn" else "kn")
    if source == target:
        raise EmptyInputError("Choose different source and target languages.")
    engine_map = engines or {"online": OnlineEngine(), "offline": OfflineEngine()}
    if preferred not in engine_map:
        raise EngineUnavailableError(f"Unknown translation engine: {preferred}")
    other = "offline" if preferred == "online" else "online"
    # Never send input to a cloud engine as an implicit fallback from Offline mode.
    order = [preferred] + (
        [other] if preferred == "online" and other in engine_map else []
    )
    failures = []
    for index, name in enumerate(order):
        try:

            def translate_sentence(sentence: str, engine_name: str = name) -> str:
                protected, replacements = apply_pre(sentence)
                translated = engine_map[engine_name].translate(
                    protected, source, target
                )
                return apply_post(translated, replacements)

            result = translate_preserving_lines(text, translate_sentence)
            return TranslationResult(result, source, target, name, fell_back=index > 0)
        except EngineUnavailableError as exc:
            failures.append(exc)
            logger.warning("Translation engine failed: %s", name)
    raise EngineUnavailableError(
        "Translation is unavailable. Check your connection or install/cache the offline model."
    ) from failures[-1]
