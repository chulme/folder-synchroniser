
from pathlib import Path
import os
from datetime import datetime, timezone
import numpy as np


class FileDiff(object):
    last_poll_time = datetime.fromtimestamp(100000)  # init to 1970-01-02

    def get_files_in_dir(self, folder_path: Path) -> list:
        files = []

        for file in Path(folder_path).iterdir():

            if file.is_dir():
                files.extend(self.get_files_in_dir(file))
            elif file.is_file():
                files.append(file)
        # self.last_poll_time = datetime.now()
        return files

    def has_file_changed(self, src: Path, dst: Path) -> bool:
        return (src.stat().st_mtime > dst.stat().st_mtime)

    def seperate_new_files(self, files: list) -> list | list:
        existing_files = []
        new_files = []
        for file in files:
            print(
                f"File:\t{file.name}\nFile Creation Time:\t{file.stat().st_ctime}\nLast Poll Time:\t\t{self.last_poll_time}\t")
            print(self.last_poll_time.timestamp())

            if(file.stat().st_ctime > self.last_poll_time.timestamp()):
                new_files.append(file)
            else:
                existing_files.append(file)

        return existing_files, new_files
