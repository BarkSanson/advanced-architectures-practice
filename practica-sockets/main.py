import socketserver
import threading
import time

HOST, PORT = 'localhost', 5000

class WaitingRoomTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True

class WaitHandler(socketserver.StreamRequestHandler):
    current_players = 0
    MAX_PLAYERS = 4
    lock = threading.Lock()
    max_players_reached = threading.Condition(lock)
    sockets = []

    def handle(self): 
        with WaitHandler.lock:
            WaitHandler.__broadcast(
                f"New player added on thread {threading.current_thread().name} from {self.client_address[0]}:{self.client_address[1]}\n")

            WaitHandler.sockets.append(self.request) 
            WaitHandler.current_players += 1

            if WaitHandler.current_players == WaitHandler.MAX_PLAYERS:
                WaitHandler.__broadcast("Max. players reached! Starting game in 5 seconds...")
                time.sleep(5)

                WaitHandler.max_players_reached.notify_all()

                self.server.shutdown()
                self.server.server_close()
                WaitHandler.__shutdown_sockets()
            else:
                WaitHandler.max_players_reached.wait()
    
    def __broadcast(msg: str):
        for sock in WaitHandler.sockets:
            sock.sendall(msg.encode("utf-8"))
    
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