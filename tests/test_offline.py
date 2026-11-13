from contextlib import nullcontext

from src.engines.offline import OfflineEngine


class FakeTokenizer:
    def __init__(self):
        self.calls = []

    def __call__(self, batch, **kwargs):
        self.calls.append(batch)
        return {"tokens": batch}

    def convert_tokens_to_ids(self, code):
        return code

    def batch_decode(self, output, skip_special_tokens):
        return [f"translated:{item}" for item in output]


class FakeModel:
    def generate(self, **kwargs):
        return kwargs["tokens"]


class FakeTorch:
    @staticmethod
    def no_grad():
        return nullcontext()


def test_offline_maps_language_codes_and_caches_resources():
    tokenizer = FakeTokenizer()
    loads = []
    engine = OfflineEngine(
        loader=lambda name: loads.append(name) or (tokenizer, FakeModel(), FakeTorch)
    )
    assert engine.translate("ನಮಸ್ಕಾರ", "kn", "en") == "translated:ನಮಸ್ಕಾರ"
    assert engine.translate("Hello", "en", "kn") == "translated:Hello"
    assert tokenizer.src_lang == "eng_Latn"
    assert loads == ["facebook/nllb-200-distilled-600M"]


def test_offline_splits_long_single_sentences_into_bounded_chunks():
    tokenizer = FakeTokenizer()
    engine = OfflineEngine(loader=lambda name: (tokenizer, FakeModel(), FakeTorch))
    engine.translate("ಅ" * 1000, "kn", "en")
    assert all(len(batch) <= 8 for batch in tokenizer.calls)
    assert all(
        len(chunk) <= engine.max_chunk_characters
        for batch in tokenizer.calls
        for chunk in batch
    )
