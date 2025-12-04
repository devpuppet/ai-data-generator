from abc import ABC, abstractmethod
from .generate_options import GenerateOptions
from .model_response import ModelResponse


class AIService(ABC):

    @abstractmethod
    def generate_response_for_insert(self, prompt: str, options: GenerateOptions) -> ModelResponse:
        pass

    @abstractmethod
    def generate_response_for_update(self, prompt: str, options: GenerateOptions) -> ModelResponse:
        pass

