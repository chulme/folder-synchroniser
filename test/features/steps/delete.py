from behave import given, when, then
from pathlib import Path
import time


def get_number_of_files_in_dir(path: Path) -> int:
    p = path.glob('**/*')
    files = [x for x in p if x.is_file()]
    return len(files)


@when(u'A synchronised file is removed from the client directory')
def step_imp(context):
    file = Path(str(context.src_path)+'\\file.txt')
    file.write_bytes(b'Hello World!')
    time.sleep(1)
    assert(get_number_of_files_in_dir(context.dst_path) == 1)
    file.unlink(missing_ok=False)  # deletes file


@then(u'The files is deleted in the server folder')
def step_imp(context):
    time.sleep(1)
    assert(get_number_of_files_in_dir(context.dst_path) == 0)
