from abc import ABC, abstractmethod
from .generate_options import GenerateOptions
from .model_response import ModelResponse


class AIService(ABC):

    @abstractmethod
    def generate_response(self, prompt: str, options: GenerateOptions) -> ModelResponse:
        pass

