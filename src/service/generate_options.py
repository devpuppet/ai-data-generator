from dataclasses import dataclass
from typing import Optional

from google.genai.types import ToolListUnion


@dataclass
class GenerateOptions:
    system_instructions: str
    tools: Optional[ToolListUnion]
    temperature: float = 1.0
    # Too low max_tokens can result in Gemini API responding with finish reason = MAX_TOKENS
    # When max_output_tokens for the Gemini client is set too low, all tokens may be used for the thinking process
    max_tokens: int = 1000