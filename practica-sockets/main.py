import socketserver
import threading

class WaitHandler(socketserver.StreamRequestHandler):
    def handle(self):
        pass

class WaitingRoom():
    MAX_PLAYERS = 4

    def __init__(self):
        self.__lock = threading.Lock()
        self.__current_players = 0

    def join(self):
        self.__current_players += 1


def main():
    waiting_room = WaitingRoom()

    with socketserver.ThreadingTCPServer(('', 3000), WaitHandler) as server:
        server.serve_forever()

if __name__ == "__main__":
    main()