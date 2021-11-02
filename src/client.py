import os
from pathlib import Path
from datetime import datetime
import socket
from threading import Thread
import time
import json


class Client(Thread):

    def __init__(self, path: Path):
        """ Initialiser for client.
        Args:
            path (Path): Path of source directory to synchronise with server.
        """
        Thread.__init__(self)

        self.source_path = Path(path)
        self.last_poll_time = datetime.fromtimestamp(
            100000)  # init to 1970-01-02
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.seen_files = []
        self.MAX_FILE_SIZE = 2147483648  # in bytes, equates to 2.15GB

    def run(self):
        """ Client entrypoint

        Created connection to server, and then:
            1. Recursively scans the source directory for new, copied, modified, and deleted files.
            2. Sends the original file path and encoded data to the server.
        """
        self.socket.connect((socket.gethostname(), 12345))

        while self.running:
            files = self.get_files_in_dir(self.source_path)

            modified_file_paths = self.get_modified_file_paths(files)
            deleted_file_paths = self.get_deleted_file_paths(files)

            files_to_send = modified_file_paths+deleted_file_paths

            if len(files_to_send) > 0:
                self.send(files_to_send)

            self.last_poll_time = datetime.now()
            time.sleep(0.5)

    @staticmethod
    def get_files_in_dir(path: Path) -> list[Path]:
        """ Recursively finds all the files in the target directory.

        Args:
            path (Path): Path of target directory to search.

        Returns:
            list: File paths found in target directory.
        """
        files = []
        for file in Path(path).iterdir():
            if file.is_dir():
                files.extend(Client.get_files_in_dir(file))
            elif file.is_file():
                files.append(file)
        return files

    def get_modified_file_paths(self, files: list[Path]) -> list[Path]:
        """ Selects files that are new, copied and modified files, while adding
            new files to the seen_files list for future reference.

        Args:
            files (list): files to determine the status of.

        Returns:
            list: File paths of modified files.
        """
        modified_file_paths = []
        new_files = []

        for file in files:
            if self.is_unseen_file(file):
                new_files.append(file)
                self.seen_files.append(file)

            elif self.has_file_changed(file):
                modified_file_paths.append(file)

        return modified_file_paths+new_files

    def has_file_changed(self, file: Path) -> bool:
        """ Determines if a file has been modified.

            This is done by inspecting the file's modification timestamp metadata.
            If the file has been updated after the last poll, the file has been modified.

        Args:
            file (Path): file to check if it has been modified.

        Returns:
            bool: Whether or not the file has been modified.
        """
        return file.stat().st_mtime > self.last_poll_time.timestamp()

    def is_unseen_file(self, path: Path) -> bool:
        """ Determines if a file is new to the client directory.

        Args:
            files (Path): file to check.

        Returns:
            bool: Whether or not the file is new.
        """
        return path not in self.seen_files

    def get_deleted_file_paths(self, files: list[Path]) -> list[Path]:
        """ Returns all paths that have been deleted, and then removes
            these elements from the seen_list.

            This is done by comparing the list of found paths in the source
            directory, against the seen_list.

        Args:
            files (list[Path]): list of paths to search over

        Returns:
            list[Path]: List of deleted files

        """
        removed_files = list(set(self.seen_files)-(set(files)))

        for file in removed_files:
            if file in self.seen_files:
                self.seen_files.remove(file)

        return removed_files

    def send(self, files: list[Path]):
        """ Sends each modified file to the server.

            Data in wrapped in a JSON format, containing the original file path and ISO8859-1 encoded data.
            The use of ISO8859-1 encoding is to provide a universal and compact format for the server to receive,
            facilitating different file types.

        Args:
            files (list[Path]): Files to send.
        """
        for file in files:
            time.sleep(0.3)  # sleep to prevent overloading the server

            relative_path = self.convert_to_relative_path(file)

            if file.exists():
                if file.stat().st_size <= self.MAX_FILE_SIZE:
                    print(f'Client sending \'{file.name}\'')
                    json_representation = json.dumps({"path": str(relative_path),
                                                      "data": file.read_bytes().decode('ISO8859-1')})
                    self.socket.send(json_representation.encode())
                else:
                    print("Warning, file is too big to be sent!")

            else:  # File doesn't exist, just send name and no data.
                json_representation = json.dumps({"path": str(relative_path)})
                self.socket.send(json_representation.encode())

    def convert_to_relative_path(self, path: Path) -> Path:
        """ Converts a given path to path relative to the source directory, such as:
            C:\\Repositories\\folder-synchroniser\\source-test-dir\\folder\\file.txt
            => folder\\file.txt

            Args:
                path (Path): Path to convert

            Returns:
                Path: The relative path to the file
        """
        full_path = str(path.resolve())
        relative_path = str(self.source_path.resolve())
        return Path(os.path.relpath(full_path, relative_path))

    def terminate(self):
        """ Called to safely stop the client.
        """

        if self.is_alive():
            self.running = False
            self.socket.close()
            print("Client terminated.")
