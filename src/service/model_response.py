from dataclasses import dataclass

@dataclass
class ModelResponse:
    text: str = None
    error: str = None