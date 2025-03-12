from dataclasses import dataclass

@dataclass
class MateSelectionConfig:
    model_name: str = 'openrouter/google/gemini-2.0-flash-001'
    timeout_seconds: int = 10
    require_integer_threshold: float = 0.01
    log_level: str = 'INFO'
