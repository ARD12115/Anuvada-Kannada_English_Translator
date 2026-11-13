class AnuvadaError(Exception):
    """Base class for user-facing application errors."""


class EmptyInputError(AnuvadaError):
    pass


class EngineUnavailableError(AnuvadaError):
    pass


class UnsupportedFileError(AnuvadaError):
    pass


class FileTooLargeError(AnuvadaError):
    pass


class OcrUnavailableError(AnuvadaError):
    pass


class SpeechError(AnuvadaError):
    pass
