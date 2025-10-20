from typing import List, Optional
from pydantic import BaseModel, Field

class CommandTemplate(BaseModel):
    command: str
    description: str
    requires_approval: bool = False
    allowed_envs: List[str] = Field(default_factory=list)

class IntentRule(BaseModel):
    intent: str  # Human-readable description
    pattern: str  # Regex pattern
    template: CommandTemplate