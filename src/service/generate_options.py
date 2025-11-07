from dataclasses import dataclass

@dataclass
class GenerateOptions:
    temperature: float = 1.0
    max_tokens: int = 100