from pathlib import Path
from datetime import datetime
import socket
from threading import Thread
import time
import json


class Client(object):
    def __init__(self, path: Path):
        self.source_path = path
        self.last_poll_time = datetime.fromtimestamp(
            100000)  # init to 1970-01-02
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.seen_files = []

    def run(self):
        self.socket.connect((socket.gethostname(), 12345))

        while self.running:
            files = self.get_files_in_dir(self.source_path)
            modified_files = self.get_modified_files(files)
            if len(modified_files) > 0:
                self.send(modified_files)
            self.last_poll_time = datetime.now()
            time.sleep(0.5)

    def get_files_in_dir(self, path: Path) -> list:
        files = []
        for file in Path(path).iterdir():
            if file.is_dir():
                files.extend(self.get_files_in_dir(file))
            elif file.is_file():
                files.append(file)
        return files

    def get_modified_files(self, files: list) -> list:
        modified_files = []
        for file in files:
            if self.is_unseen_file(file) or self.has_file_changed(file):
                modified_files.append(file)
                self.seen_files.append(file)
        return modified_files

    def has_file_changed(self, src: Path) -> bool:
        return src.stat().st_mtime > self.last_poll_time.timestamp()

    def is_unseen_file(self, path: Path) -> bool:
        return (path not in self.seen_files)

    def send(self, files: list) -> bool:
        for file in files:
            time.sleep(0.1)
            print(f'Client sending \'{file.name}\'')
            json_representation = json.dumps({"path": str(file),
                                              "data": file.read_bytes().decode('ISO8859-1')})
            self.socket.send(json_representation.encode())

    def terminate(self):
        self.running = False
        self.socket.close()
