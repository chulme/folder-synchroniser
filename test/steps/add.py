from behave import given, when, then
from pathlib import Path
import time

import sys
import os
import shutil

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\\..\\..\\src")

import client as cl
import server as srv
import filediff

@given(u'Client and server are ran concurrently')
def step_imp(context):
    client = cl.Client(Path('..\\build\\src'))
    server= srv.Server(Path('..\\dst\\src'))
    server.start()
    client.start()
    print("Nodes started")

    # Terminate nodes after 5s. To-do, move to seperate then block
    time.sleep(5)
    server.terminate()
    client.terminate()


@when(u'A file is saved in the client directory')
def step_imp(context):
    Path('..\\build\\src').mkdir(parents=True,exist_ok=True)
    Path('..\\build\\dst').mkdir(parents=True, exist_ok=True)
    file = Path('..\\build\\src\\file.txt')
    file.write_bytes(b'Hello World!')
    print("File saved in client dir")


@when(u'A file is saved within a folder of the client directory')
def step_imp(context):
    shutil.rmtree(Path('..\\build'))
    Path('..\\build\\src\\my_folder').mkdir(parents=True, exist_ok=False)
    Path('..\\build\\dst').mkdir(parents=True, exist_ok=False)
    file = Path('..\\build\\src\\my_folder\\file.txt')
    file.open("w", encoding = "utf-8").write('Hello World!')
    print("File saved within folder of client dir")


@when(u'The file is copied and pasted in the client directory')
def step_imp(context):
    shutil.copy(Path('..\\build\\src\\file.txt'), '..\\build\\src\\file2.txt')
    print("File copied")


@then(u'The files are synchronised in the server folder')
def step_imp(context):
    files = filediff.FileDiff().get_files_in_dir('..\\build\\src')
    assert len(files)>0
    for file in files:
        dst_equivalent = Path(str(file).replace("src", "dst"))
        assert file.read_bytes() == dst_equivalent.read_bytes()
    print("Files synced")


@then(u'Concurrent threads are joined')
def step_imp(context):
    print("Not implemented")



    
