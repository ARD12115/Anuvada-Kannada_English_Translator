from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from threading import Event
from time import sleep

from src.engines.offline import OfflineEngine


class FakeTokenizer:
    def __init__(self):
        self.src_lang = None
        self.calls = []
        self.input_chunks = []

    def __call__(self, text, **kwargs):
        assert kwargs["max_length"] == 512
        assert kwargs["padding"] is True
        assert kwargs["truncation"] is True
        assert kwargs["return_overflowing_tokens"] is True
        assert kwargs["stride"] == 0
        chunks = [
            list(text[start : start + kwargs["max_length"]])
            for start in range(0, len(text), kwargs["max_length"])
        ]
        if not chunks:
            chunks = [[]]
        self.input_chunks.extend(chunks)
        self.calls.append((self.src_lang, text))
        return {
            "input_ids": chunks,
            "attention_mask": [[1] * len(chunk) for chunk in chunks],
            "overflow_to_sample_mapping": [0] * len(chunks),
        }

    def convert_tokens_to_ids(self, code):
        return code

    def batch_decode(self, output, skip_special_tokens):
        return ["".join(item) for item in output]


class FakeModel:
    def generate(self, **kwargs):
        assert "overflow_to_sample_mapping" not in kwargs
        return kwargs["input_ids"]


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
    assert engine.translate("ನಮಸ್ಕಾರ", "kn", "en") == "ನಮಸ್ಕಾರ"
    assert engine.translate("Hello", "en", "kn") == "Hello"
    assert tokenizer.calls == [("kan_Knda", "ನಮಸ್ಕಾರ"), ("eng_Latn", "Hello")]
    assert loads == ["facebook/nllb-200-distilled-600M"]


def test_offline_translates_every_token_overflow_segment():
    tokenizer = FakeTokenizer()
    engine = OfflineEngine(loader=lambda name: (tokenizer, FakeModel(), FakeTorch))
    source = "ಅ" * 1200
    result = engine.translate(source, "kn", "en")
    assert result.replace(" ", "") == source
    assert "".join("".join(chunk) for chunk in tokenizer.input_chunks) == source
    assert max(map(len, tokenizer.input_chunks)) <= 512


def test_shared_tokenizer_source_language_is_isolated_across_threads():
    first_started = Event()
    release_first = Event()

    class BlockingTokenizer(FakeTokenizer):
        def __init__(self):
            super().__init__()
            self.call_count = 0

        def __call__(self, text, **kwargs):
            self.call_count += 1
            call_number = self.call_count
            if call_number == 1:
                first_started.set()
                release_first.wait(timeout=2)
            return super().__call__(text, **kwargs)

    tokenizer = BlockingTokenizer()
    engine = OfflineEngine(loader=lambda name: (tokenizer, FakeModel(), FakeTorch))
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(engine.translate, "ಕನ್ನಡ", "kn", "en")
        assert first_started.wait(timeout=2)
        second = pool.submit(engine.translate, "English", "en", "kn")
        sleep(0.05)
        release_first.set()
        first.result(timeout=2)
        second.result(timeout=2)
    assert tokenizer.calls == [("kan_Knda", "ಕನ್ನಡ"), ("eng_Latn", "English")]
