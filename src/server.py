from pathlib import Path
import socket
from threading import Thread
import json


class Server(Thread):
    def __init__(self, path: Path):
        """ Initialiser for server.
        Args:
            path (Path): Path of source directory to synchronise with server.
        """
        Thread.__init__(self, daemon=False)
        self.destination_path = path
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 12345))
        self.running = True

    def run(self):
        """ Server entrypoint

        Establishes connection to client, and then receives JSON messages containing
        the original file path and the file's encoded data. These fields are then used
        to save the file in the appropriate location within the destination directory.
        """
        self.socket.listen()
        conn, addr = self.socket.accept()
        print('Client-server connection established on', addr)
        while self.running:
            msg = conn.recv(2147483648)  # 2.15 GB
            if not msg:
                break
            json_representation = json.loads(msg)
            self.save(json_representation)
        conn.close()
        print("Client-server connection closed.")

    @staticmethod
    def save(file: dict[str, str]):
        """ Saves received files to the destination directory.

        Args:
            file (dict[str,str]): Original file path and encoded data to save.
        """
        dst_path = Server.convert_src_to_dst_path(Path(file["path"]))
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        if("data" in file):
            print(f'Server saving {dst_path}')
            dst_path.write_bytes(bytes(file["data"], 'ISO8859-1'))
        else:
            print(f'Server deleting {dst_path}')
            dst_path.unlink(missing_ok=True)

    @staticmethod
    def convert_src_to_dst_path(path: Path) -> Path:
        """ Converts the received original path of a file, to the equivalent location
            in the destination folder.
        """
        return Path(str(path).replace("src", "dst"))

    def terminate(self):
        """ Called to safely stop the server.
        """
        print("Server terminating.")
        self.running = False
        self.socket.close()
