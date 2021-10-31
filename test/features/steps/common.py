from pathlib import Path
from behave import given, when, then
import threading
from src import client as cl
from src import server as srv


def get_number_of_files_in_dir(path: Path) -> int:
    p = path.glob('**/*')
    files = [x for x in p if x.is_file()]
    return len(files)


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


@then(u'Concurrent threads are joined')
def step_imp(context):
    context.server.terminate()
    context.client.terminate()
    context.server_thread.join()
