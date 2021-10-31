"""When A large file is saved in the client directory
Then The file is not sent"""
from pathlib import Path
from behave import given, when, then
import time
import steps.common as Common

"""
    path = str(context.src_path.resolve())+'\my_file'
    print(path)
    with open(path, 'wb') as f:
        num_chars = 1024 * 1024 * 1024*3
        f.write(b'0' * num_chars)
    time.sleep(10)
    assert(Common.get_number_of_files_in_dir(context.dst_path) == 1)
    assert(file.stat().st_size > 2147483648)"""


@when(u'A large file is saved in the client directory')
def step_imp(context):
    file = Path(str(context.src_path)+'\\large-file.txt')
    file.write_bytes(b'0'*(3*1024 * 1024*1024))  # creates 3GB file
    time.sleep(1)
    assert(Common.get_number_of_files_in_dir(context.src_path) == 1)
    assert(file.stat().st_size > 2147483648)


@ then(u'The file is not synchronised with the server')
def step_imp(context):
    time.sleep(1)
    assert(Common.get_number_of_files_in_dir(context.dst_path) == 0)
