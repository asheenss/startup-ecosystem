from typing import Any

from pydantic import BaseModel, Field


class ProtocolMessage(BaseModel):
    sender: str
    task: str
    data: dict[str, Any] = Field(default_factory=dict)
    memory: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)


class ProtocolResponse(BaseModel):
    sender: str
    status: str = "success"
    data: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
