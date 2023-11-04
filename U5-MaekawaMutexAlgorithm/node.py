from threading import Event, Thread, Timer
from datetime import datetime, timedelta
from enum import Enum
import time

from nodeServer import NodeServer
from nodeSend import NodeSend
from message import Message, MessageType
import config

class NodeState(Enum):
    RELEASED = 0
    WANTED = 1
    HELD = 2

class Node():
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id
        self.port = config.port + id
        self.daemon = True
        self.lamport_ts = 0
        
        self.server = NodeServer(self)
        self.server.start()

        if id % 2 == 0:
            self.colleagues = list(range(0, config.numNodes, 2))
        else:
            self.colleagues = list(range(1, config.numNodes, 2))

        self.client = NodeSend(self)

    def do_connections(self):
        self.client.build_connection()

    def state(self):
        timer = Timer(1, self.state)  # Each 1s the function call itself
        timer.start()
        self.curr_time = datetime.now()
        # TODO something

        self.my_state = NodeState.RELEASED
        self.voted = False
        self.request_queue = []

        self.wakeupcounter += 1
        if self.wakeupcounter == 2:
            timer.cancel()
            print("Stopping N%i" % self.id)
            self.daemon = False
        else:
            print("This is Node_%i at TS:%i sending a message to my collegues" % (self.id, self.lamport_ts))

            message = Message(MessageType.GREETING,
                              self.id,
                              "Hola, this is Node_%i _ counter:%i" % (self.id, self.wakeupcounter))

            self.client.multicast(message, self.colleagues)

    def run(self):
        print("Run Node%i with the follows %s" % (self.id, self.colleagues))
        self.client.start()
        self.wakeupcounter = 0
        self.state()

    def handle_request(self, msg):
        if self.my_state == NodeState.HELD or self.voted:
            self.request_queue.append(msg)
        else:
            self.voted = True
            reply = Message(MessageType.REPLY, self.id, "Ok", msg.src, self.lamport_ts)
            self.client.send_message(reply, msg.src)

    def handle_release(self, msg):
        if self.request_queue:
            next_request = self.request_queue.pop(0)
            reply = Message(MessageType.REPLY, self.id, "Ok", next_request.src, self.lamport_ts)
            self.client.send_message(reply, next_request.src)
        else:
            self.voted = False

    def handle_reply(self, msg):
        pass
