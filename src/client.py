from pathlib import Path
from datetime import datetime
import socket
from threading import Thread
import time
import json


class Client(Thread):
    def __init__(self, path: Path):
        Thread.__init__(self)

        self.source_path = path
        self.last_poll_time = datetime.fromtimestamp(
            100000)  # init to 1970-01-02
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("New client thread created.")

    def run(self):
        self.socket.connect((socket.gethostname(), 12345))

        while True:
            files = self.get_files_in_dir()
            modified_files = self.get_modified_files(files)
            if len(modified_files) > 0:
                self.send(files)
            self.last_poll_time = datetime.now()
            time.sleep(1)

    def get_files_in_dir(self) -> list:
        files = []
        for file in Path(self.source_path).iterdir():
            if file.is_dir():
                files.extend(self.get_files_in_dir(file))
            elif file.is_file():
                files.append(file)
        return files

    def get_modified_files(self, files: list) -> list:
        modified_files = []
        for file in files:
            if self.has_file_changed(file):
                modified_files.append(file)
        return modified_files

    def has_file_changed(self, src: Path) -> bool:
        return (src.stat().st_mtime > self.last_poll_time.timestamp())

    def send(self, files: list) -> bool:
        for file in files:
            json_representation = json.dumps({"path": str(file),
                                              "data": file.read_bytes().decode()})
            self.socket.send(json_representation.encode())
