import socketserver
import threading
import time

HOST, PORT = 'localhost', 5000


class WaitingRoomTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


class WaitHandler(socketserver.StreamRequestHandler):
    current_players = 0
    MAX_PLAYERS = 4
    lock = threading.Lock()
    # Condition variable to sleep/wake threads
    max_players_reached = threading.Condition(lock)
    sockets = []

    def handle(self):
        self.request.sendall("Welcome!\n".encode("utf-8"))

        with WaitHandler.lock:
            WaitHandler.__broadcast(
                f"New player added from {self.client_address[0]}:{self.client_address[1]}!\n")

            WaitHandler.current_players += 1

            WaitHandler.sockets.append(self.request)
            WaitHandler.__broadcast(
                f"Remaining players {WaitHandler.MAX_PLAYERS - WaitHandler.current_players}\n")

            if WaitHandler.current_players == WaitHandler.MAX_PLAYERS:
                WaitHandler.__broadcast("Max. players reached! Starting game in 5 seconds...")
                time.sleep(5)

                # Wake all threads
                WaitHandler.max_players_reached.notify_all()

                WaitHandler.__shutdown_sockets()
                self.server.shutdown()
                self.server.server_close()
            else:
                # Go to sleep
                WaitHandler.max_players_reached.wait()

    @staticmethod
    def __broadcast(msg: str):
        for sock in WaitHandler.sockets:
            sock.sendall(msg.encode("utf-8"))

    @staticmethod
    def __shutdown_sockets():
        for sock in WaitHandler.sockets:
            sock.close()


def main():
    server = WaitingRoomTCPServer((HOST, PORT), WaitHandler)

    try:
        print(f"Server listening on port {PORT}")
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
