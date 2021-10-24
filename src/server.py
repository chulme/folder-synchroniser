from pathlib import Path
import socket
from threading import Thread
import json

class Server(Thread):
    def __init__(self, path: Path):
        Thread.__init__(self)
        print("New server thread created.")

        self.destination_path = path
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 12345))
        self.running=True

    def run(self):
        self.socket.listen()
        conn, addr = self.socket.accept()
        print('Client-server connection established on', addr)
        while self.running:
            msg = conn.recv(9999999999)
            if not msg:
                break
            print(msg)
            json_representation = json.loads(msg)
            self.save(json_representation)
        conn.close()
        print("Client-server connection closed.")


    def save(self, file: dict):
        dst_path = self.convert_src_to_dst_path(Path(file["path"]))
        print(f'Server saving {dst_path.name}')
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        dst_path.write_bytes(bytes(file["data"], 'ISO8859-1'))

    def convert_src_to_dst_path(self, path: Path) -> Path:
        return Path(str(path).replace("src", "dst"))

    def terminate(self):
        self.running = False
        self.socket.close()
