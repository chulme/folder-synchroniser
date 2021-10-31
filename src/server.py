from pathlib import Path, PurePath
import socket
from threading import Thread
import json


class Server(Thread):
    def __init__(self, path: Path):
        """ Initialiser for server.
        Args:
            path (Path): Path of source directory to synchronise with server.
        """
        Thread.__init__(self)
        self.destination_path = Path(path)
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

    def save(self, file: dict[str, str]):
        """ Saves received files to the destination directory.

        Args:
            file (dict[str,str]): Original file path and encoded data to save.
        """
        dst_path = self.convert_to_dst_path(Path(file["path"]))

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        if("data" in file):
            print(f'Server saving {dst_path}')
            dst_path.write_bytes(bytes(file["data"], 'ISO8859-1'))
        else:
            print(f'Server deleting {dst_path}')
            dst_path.unlink(missing_ok=True)

    def convert_to_dst_path(self, path: Path) -> Path:
        """ Converts the relative path of a file, to the full path
            in the destination folder.
        """
        return Path(self.destination_path, path)

    def terminate(self):
        if self.is_alive():
            """ Called to safely stop the server.
            """
            self.running = False
            self.socket.close()
            print("Server terminated.")
