import json
import enum

from dataclasses import dataclass


class MessageType(enum.Enum):
    GREETING = "Greeting"
    REQUEST = "Request"
    REPLY = "Reply"
    RELEASE = "Release"


@dataclass
class Message(object):
    msg_type: MessageType
    src: int
    data: str
    dest: int = None
    ts: int = None

    def __json__(self):
        return dict(msg_type=self.msg_type,
                    src=self.src,
                    dest=self.dest,
                    ts=self.ts,
                    data=self.data)

    @classmethod
    def from_json(cls, json_str) -> 'Message':
        obj_dict = json.loads(json_str)
        msg = cls(MessageType(obj_dict['msg_type']),
                      obj_dict['src'],
                      obj_dict['dest'],
                      obj_dict['ts'],
                      obj_dict['data'])

        return msg

    def to_json(self):
        obj_dict = dict()
        obj_dict['msg_type'] = self.msg_type.value
        obj_dict['src'] = self.src
        obj_dict['dest'] = self.dest
        obj_dict['ts'] = self.ts
        obj_dict['data'] = self.data
        return json.dumps(obj_dict)
