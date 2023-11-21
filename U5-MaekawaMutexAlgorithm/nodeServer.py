import select
from threading import Thread
import utils
from message import Message
import json

from message import Message, MessageType


class NodeServer(Thread):
    def __init__(self, node):
        Thread.__init__(self)
        self.node = node
        self.connection_list = []
        self.server_socket = utils.create_server_socket(self.node.port)
        self.connection_list.append(self.server_socket)

    def run(self):
        self.update()

    def update(self):
        while self.node.daemon:
            (read_sockets, write_sockets, error_sockets) = select.select(
                self.connection_list, [], [], 5)
            if not (read_sockets or write_sockets or error_sockets):
                pass
            else:
                for read_socket in read_sockets:
                    if read_socket == self.server_socket:
                        (conn, addr) = read_socket.accept()
                        self.connection_list.append(conn)
                    else:
                        try:
                            msg_stream, _ = read_socket.recvfrom(4096)
                            try:
                                ms = json.loads(msg_stream)
                                self.process_message(ms)
                            except Exception as e:
                                print("Error processing message", e.with_traceback())
                        except:
                            read_socket.close()
                            self.connection_list.remove(read_socket)
                            continue

        self.server_socket.close()
        print("Closing Server socket")

    def process_message(self, msg):
        msg = Message.from_json(msg)

        # print("Node_%i receive msg: %s" % (self.node.id, msg))

        if msg.msg_type == MessageType.REQUEST:
            self.node.handle_request(msg)
        elif msg.msg_type == MessageType.RELEASE:
            self.node.handle_release()
        elif msg.msg_type == MessageType.REPLY:
            self.node.handle_reply()
