from _socket import _RetAddress
from collections.abc import Callable
import socketserver
from socketserver import _AfInetAddress, BaseRequestHandler
import threading
import time
from typing import Any

HOST, PORT = 'localhost', 3000

class WaitingRoomTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    MAX_PLAYERS = 4

    def __init__(self, 
                 server_address, 
                 RequestHandlerClass, 
                 bind_and_activate = True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

class WaitHandler(socketserver.StreamRequestHandler):
    current_players = 0
    MAX_PLAYERS = 4
    lock = threading.Lock()
    sockets = []

    def handle(self): 
        with WaitHandler.lock:
            WaitHandler.sockets.append(self.request) 
            WaitHandler.current_players += 1




def main():
    server = WaitingRoomTCPServer((HOST, PORT), WaitHandler) 

    try:
        print(f"Server listening on port {PORT}")

        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    main()