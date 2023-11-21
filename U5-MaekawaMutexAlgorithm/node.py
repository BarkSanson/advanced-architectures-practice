from threading import Thread, Condition
from enum import Enum
import time
import random

from nodeServer import NodeServer
from nodeSend import NodeSend
from message import Message, MessageType
import config


class NodeState(Enum):
    RELEASED = 0
    WANTED = 1
    HELD = 2


class Node(Thread):
    _FINISHED_NODES = 0
    _HAVE_ALL_FINISHED = Condition()

    def __init__(self, node_id, k):
        Thread.__init__(self)
        self.id = node_id
        self.port = config.port + self.id
        self.daemon = True
        self.lamport_ts = 0

        self.k = k

        self.votes_received = 0
        self.my_state = NodeState.RELEASED
        self.voted = False
        self.request_queue = []

        self.server = NodeServer(self)
        self.server.start()

        if self.id % 2 == 0:
            self.colleagues = list(range(0, config.numNodes, 2))
        else:
            self.colleagues = list(range(1, config.numNodes, 2))

        if len(self.colleagues) < self.k:
            random_colleague = random.randint(0, config.numNodes - 1)
            while random_colleague in self.colleagues or random_colleague == self.id:
                random_colleague = (random_colleague + 1) % config.numNodes

            self.colleagues.append(random_colleague)

        self.client = NodeSend(self)

    def do_connections(self):
        self.client.build_connection()

    def run(self):
        print("Run Node%i with the follows %s" % (self.id, self.colleagues))
        self.client.start()

        print("This is Node_%i at TS:%i sending a message to my collegues" % (self.id, self.lamport_ts))
        message = Message(MessageType.GREETING, self.id)
        self.client.multicast(message, self.colleagues)

        # So that the nodes don't start at the same time
        time_offset = random.randint(2, 8)
        time.sleep(time_offset)

        self._lock()

        simulated_time_in_cs = random.randint(0, 5)
        time.sleep(simulated_time_in_cs)

        self._unlock()

        print("****Node_%i at TS:%i is done" % (self.id, self.lamport_ts))

        # Wait all nodes to finish
        with Node._HAVE_ALL_FINISHED:
            Node._FINISHED_NODES += 1
            if Node._FINISHED_NODES == config.numNodes:
                Node._HAVE_ALL_FINISHED.notify_all()

            while Node._FINISHED_NODES < config.numNodes:
                Node._HAVE_ALL_FINISHED.wait()

        print("****Node_%i at TS:%i is exiting" % (self.id, self.lamport_ts))

        # self.state()

    def handle_request(self, msg):
        if self.my_state == NodeState.HELD or self.voted:
            self.request_queue.append(msg)
        else:
            reply = Message(MessageType.REPLY, self.id, msg.src)
            self.client.send_message(reply, reply.dest)
            self.voted = True

    def handle_release(self):
        if self.request_queue:
            next_request = self.request_queue.pop(0)
            reply = Message(MessageType.REPLY, self.id, next_request.src)
            self.client.send_message(reply, reply.dest)
            self.voted = True
        else:
            self.voted = False

    def handle_reply(self):
        self.votes_received += 1

    def _lock(self):
        print("Node_%i at TS:%i is requesting the resource" % (self.id, self.lamport_ts))
        self.my_state = NodeState.WANTED
        message = Message(MessageType.REQUEST, self.id)
        self.client.multicast(message, self.colleagues)

        while not self.votes_received == self.k:
            pass

        self.my_state = NodeState.HELD
        self.votes_received = 0

        print("Node_%i at TS:%i is holding the resource" % (self.id, self.lamport_ts))

    def _unlock(self):
        self.my_state = NodeState.RELEASED
        message = Message(MessageType.RELEASE, self.id)
        self.client.multicast(message, self.colleagues)
        self.replies_received = 0
        print("Node_%i at TS:%i is releasing the resource" % (self.id, self.lamport_ts))
