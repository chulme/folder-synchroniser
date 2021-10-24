from pathlib import Path
from datetime import datetime
import socket
from threading import Thread
import time
import json


class Client(object):

    def __init__(self, path: Path):
        """ Constructor for client.
        Args:
            path (Path): Path of source directory to synchronise with server.
        """
        self.source_path = path
        self.last_poll_time = datetime.fromtimestamp(
            100000)  # init to 1970-01-02
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.seen_files = []

    def run(self):
        """ Client entrypoint

        Created connection to server, and then:
            1. Recursively scans the source directory for new, copied, modified, and deleted files.
            2. Sends the original file path and encoded data to the server.
        """
        self.socket.connect((socket.gethostname(), 12345))

        while self.running:
            files = self.get_files_in_dir(self.source_path)
            modified_files = self.get_modified_files(files)
            if len(modified_files) > 0:
                self.send(modified_files)
            self.last_poll_time = datetime.now()
            time.sleep(0.5)

    def get_files_in_dir(self, path: Path) -> list:
        """ Recursively finds all the files in the target directory.

        Args:
            path (Path): Path of target directory to search.

        Returns:
            list: File paths found in target directory.
        """
        files = []
        for file in Path(path).iterdir():
            if file.is_dir():
                files.extend(self.get_files_in_dir(file))
            elif file.is_file():
                files.append(file)
        return files

    def get_modified_files(self, files: list) -> list:
        """ Selects files that have been copied, modified, and deleted files.

            This is done in a single function/loop for efficiency.

        Args:
            files (list): files to determine the status of.

        Returns:
            list: File paths of modified files.
        """
        modified_files = []
        for file in files:
            if self.is_unseen_file(file) or self.has_file_changed(file):
                modified_files.append(file)
                self.seen_files.append(file)
        return modified_files

    def has_file_changed(self, file: Path) -> bool:
        """ Determines if a file has been modified.

            This is done by inspecting the file's modification timestamp metadata.
            If the file has been updated after the last poll, the file has been modified.

        Args:
            files (Path): file to check if it has been modified.

        Returns:
            bool: Whether or not the file has been modified.
        """
        return file.stat().st_mtime > self.last_poll_time.timestamp()

    def is_unseen_file(self, path: Path) -> bool:
        """ Determines if a file is new to the client.

        Args:
            files (Path): file to check.

        Returns:
            bool: Whether or not the file is new.
        """
        return (path not in self.seen_files)

    def send(self, files: list):
        """ Sends each modified file to the server.

            Data in wrapped in a JSON format, containing the original file path and ISO8859-1 encoded data.
            The use of ISO8859-1 encoding is because I've found it to be the most compatible with different
            file types.

        Args:
            files (list): Files to send.
        """
        for file in files:
            time.sleep(0.1)
            print(f'Client sending \'{file.name}\'')
            json_representation = json.dumps({"path": str(file),
                                              "data": file.read_bytes().decode('ISO8859-1')})
            self.socket.send(json_representation.encode())

    def terminate(self):
        """ Called to safely stop the client.
        """
        self.running = False
        self.socket.close()
