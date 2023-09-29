import socketserver
import threading

HOST, PORT = 'localhost', 3000

class WaitingRoom():
    MAX_PLAYERS = 4

    def __init__(self):
        self.__lock = threading.Lock()
        self.__current_players = 0

    def join(self):
        with self.__lock.acquire():
            self.__current_players += 1
            print(f"Player added! Total players: {self.__current_players}")

class WaitHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server, waiting_room: WaitingRoom):
        super().__init__(request, client_address, server)
        self.__waiting_room = waiting_room

    def handle(self):
        self.__waiting_room.join()

def main():
    waiting_room = WaitingRoom()

    with socketserver.ThreadingTCPServer((HOST, PORT), \
        lambda *args, **kwargs: \
            WaitHandler(*args, **kwargs, waiting_room=waiting_room)) as server:
        print(f"Listening on port {PORT}")
        server.serve_forever()

if __name__ == "__main__":
    main()