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
    __msg_type: MessageType
    __src: int
    __data: str
    __dest: int = None
    __ts: int = None

    @property
    def msg_type(self):
        return self.__msg_type

    @msg_type.setter
    def msg_type(self, msg_type):
        self.__msg_type = msg_type

    @property
    def src(self):
        return self.__src

    @src.setter
    def src(self, src):
        self.__src = src

    @property
    def dest(self):
        return self.__dest

    @dest.setter
    def dest(self, dest):
        self.__dest = dest

    @property
    def ts(self):
        return self.__ts

    @ts.setter
    def ts(self, ts):
        self.__ts = ts

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

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
