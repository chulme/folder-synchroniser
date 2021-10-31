import shutil
from behave import given, when, then
from pathlib import Path
import time
from src import client as cl
from src import server as srv


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
    time.sleep(2)
    files = cl.Client.get_files_in_dir(context.src_path)

    assert len(files) > 0
    for file in files:
        dst_equivalent = Path(str(file).replace("src", "dst"))
        assert file.read_bytes() == dst_equivalent.read_bytes()
