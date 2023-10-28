import json

from dataclasses import dataclass, asdict


@dataclass(frozen=True, )
class Message:
    player: str
    row: int
    col: int

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_message) -> 'Message':
        return cls(**json.loads(json_message))
