from dataclasses import dataclass

@dataclass
class GenerateOptions:
    temperature: float = 1.0
    # Too low max_tokens can result in Gemini API responding with finish reason = MAX_TOKENS
    # When max_output_tokens for the Gemini client is set too low, all tokens may be used for the thinking process
    max_tokens: int = 1000