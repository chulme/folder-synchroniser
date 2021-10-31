import sys
import os
import shutil

sys.path.append(os.path.dirname(
    os.path.realpath(__file__)) + "\\..\\..\\..\\src")


import client as cl
import server as srv
import environment
from behave import given, when, then
from pathlib import Path
import time
import threading



@given(u'Source-destination folders are created')
def step_imp(context):
    context.src_path = Path('test\\build\\test'+context.scenario.name+'\\src')
    context.dst_path = Path('test\\build\\test'+context.scenario.name+'\\dst')
    context.src_path.mkdir(parents=True, exist_ok=True)
    context.dst_path.mkdir(parents=True, exist_ok=True)


@given(u'Client and server are ran concurrently')
def step_imp(context):
    context.server = srv.Server(context.dst_path)
    context.client = cl.Client(context.src_path)

    context.server_thread = threading.Thread(target=context.server.run)
    context.client_thread = threading.Thread(target=context.client.run)

    context.server_thread.start()
    context.client_thread.start()


@when(u'A file is saved in the client directory')
def step_imp(context):
    file = Path(str(context.src_path)+'\\file.txt')
    file.write_bytes(b'Hello World!')
    time.sleep(0.5)


@when(u'A file is saved within a folder of the client directory')
def step_imp(context):
    Path(str(context.src_path)+'\\my_folder').mkdir(parents=True, exist_ok=True)
    file = Path(str(context.src_path)+'\\my_folder\\file.txt')
    file.open("w", encoding="utf-8").write('Hello World!')
    time.sleep(0.5)


@when(u'The file is copied and pasted in the client directory')
def step_imp(context):
    shutil.copy2(Path(str(context.src_path)+'\\file.txt'),
                 str(context.src_path)+'\\file2.txt')


@then(u'The files are synchronised in the server folder')
def step_imp(context):
    time.sleep(1)
    files = cl.Client.get_files_in_dir(context.src_path)

    assert len(files) > 0
    for file in files:
        dst_equivalent = Path(str(file).replace("src", "dst"))
        assert file.read_bytes() == dst_equivalent.read_bytes()


@then(u'Concurrent threads are joined')
def step_imp(context):
    context.server.terminate()
    context.client.terminate()
    context.server_thread.join()
