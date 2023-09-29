import socketserver
import threading
import time

HOST, PORT = 'localhost', 3000

class WaitingRoom():
    MAX_PLAYERS = 4

    def __init__(self):
        self.__current_players = 0
        self.__lock = threading.Lock()
        self.__is_full = threading.Condition(self.__lock)

    @property
    def current_players(self):
        return self.__current_players
    
    def wait(self):
        with self.__lock:
            while self.__current_players < WaitingRoom.MAX_PLAYERS:
                self._is_full.wait()
            self.__is_full.notify()

    def join(self):
        with self.__lock:
            self.__current_players += 1
            return self.__current_players


class WaitHandler(socketserver.StreamRequestHandler):
    waiting_room = WaitingRoom()
    connections = []

    def handle(self):
        WaitHandler.connections.append(self)
        WaitHandler.waiting_room.join()
        print("Player connected")
        self.__broadcast(f"One player connected. Remaining players: \
                         {WaitingRoom.MAX_PLAYERS - WaitHandler.waiting_room.current_players}")
        
        WaitHandler.waiting_room.wait()
        
        if (WaitHandler.waiting_room.current_players >= WaitingRoom.MAX_PLAYERS):
            self.__broadcast("Number of players reached. Starting game...")
            time.sleep(2)
    
    def __broadcast(self, msg):
        for c in WaitHandler.connections:
            if c != self:
                try:
                    c.wfile.write(msg.encode("utf-8"))
                except Exception as e:
                    print(e)


def main():
    server = socketserver.ThreadingTCPServer((HOST, PORT), WaitHandler)
    try:
        print(f"Server listening on port {PORT}")
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    main()