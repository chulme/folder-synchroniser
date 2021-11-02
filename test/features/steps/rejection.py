from pathlib import Path
from behave import given, when, then
import time
import steps.common as Common


@when(u'A large file is saved in the client directory')
def step_imp(context):
    file = Path(str(context.src_path)+'\\large-file.txt')
    file.write_bytes(b'0'*(3*1024 * 1024*1024))  # creates 3GB file
    time.sleep(1)
    assert(Common.get_number_of_files_in_dir(context.src_path) == 1)
    assert(file.stat().st_size > 2147483648)


@when(u'The large file is deleted')
def step_imp(context):
    Path(str(context.src_path)+'\\large-file.txt').unlink()


@then(u'The file is not synchronised with the server')
def step_imp(context):
    time.sleep(1)
    assert(Common.get_number_of_files_in_dir(context.dst_path) == 0)
