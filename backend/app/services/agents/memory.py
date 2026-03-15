class AgentMemory:
    def __init__(self) -> None:
        self._memory: dict[str, dict] = {}

    def get(self, key: str) -> dict:
        return self._memory.get(key, {})

    def set(self, key: str, value: dict) -> None:
        self._memory[key] = value

    def snapshot(self) -> dict:
        return dict(self._memory)
