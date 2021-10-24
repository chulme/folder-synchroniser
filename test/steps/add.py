from behave import given, when, then
from pathlib import Path

import sys
import os
import shutil

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\\..\\..\\src")

import client as cl
import server as srv
import filediff

@given(u'Client and server are initialised')
def step_imp(context):
    client = cl.Client()
    server= srv.Server()

@when(u'A file is saved in the client directory')
def step_imp(context):
    Path('..\\build\\src').mkdir(parents=True,exist_ok=True)
    Path('..\\build\\dst').mkdir(parents=True, exist_ok=True)
    file = Path('..\\build\\src\\file.txt')
    file.write_bytes(b'Hello World!')

@when(u'A file is saved within a folder of the client directory')
def step_imp(context):
    shutil.rmtree(Path('..\\build'))
    Path('..\\build\\src\\my_folder').mkdir(parents=True, exist_ok=False)
    Path('..\\build\\dst').mkdir(parents=True, exist_ok=False)
    file = Path('..\\build\\src\\my_folder\\file.txt')
    file.open("w", encoding = "utf-8").write('Hello World!')


@when(u'The file is copied and pasted in the client directory')
def step_imp(context):
    shutil.copy(Path('..\\build\\src\\file.txt'), '..\\build\\src\\file2.txt')


@then(u'The files are synchronised in the server folder')
def step_imp(context):
    files = filediff.FileDiff().get_files_in_dir('..\\build\\src')
    for file in files:
        dst_equivalent = Path(str(file).replace("src", "dst"))
        assert file.read_bytes() == dst_equivalent.read_bytes()

    
