from abc import ABC, abstractmethod
from .generate_options import GenerateOptions


class AIService(ABC):

    @abstractmethod
    def generate_response(self, prompt: str, options: GenerateOptions):
        pass

