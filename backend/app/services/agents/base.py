from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.agents.protocol import ProtocolMessage, ProtocolResponse


class BaseAgent(ABC):
    name: str

    @abstractmethod
    def run(self, message: ProtocolMessage) -> ProtocolResponse:
        raise NotImplementedError
