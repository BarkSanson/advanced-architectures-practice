import json
import enum

from dataclasses import dataclass


class MessageType(enum.Enum):
    GREETING = "Greeting"
    REQUEST = "Request"
    RELEASE = "Release"
    REPLY = "Reply"


@dataclass
class Message(object):
    msg_type: MessageType
    src: int
    dest: int = None
    ts: int = None

    def __json__(self):
        return dict(msg_type=self.msg_type,
                    src=self.src,
                    dest=self.dest,
                    ts=self.ts)

    @classmethod
    def from_json(cls, json) -> 'Message':
        msg = cls(MessageType(json['msg_type']),
                  json['src'],
                  json['dest'],
                  json['ts'])

        return msg

    def to_json(self):
        obj_dict = dict()
        obj_dict['msg_type'] = self.msg_type.value
        obj_dict['src'] = self.src
        obj_dict['dest'] = self.dest
        obj_dict['ts'] = self.ts
        return json.dumps(obj_dict)
