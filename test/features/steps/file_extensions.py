from pathlib import Path, PurePath
from behave import given, when, then
from src import client as cl
from src import server as srv
import shutil
import time


@when(u'A .mp4 file is saved in the client directory')
def step_imp(context):
    original_path = Path('test\\files\\vid\\malyasia.mp4')
    copied_path = Path(str(context.src_path)+'\\malyasia.mp4')
    shutil.copy(original_path, copied_path)
    time.sleep(1)


@when(u'A .avi file is saved in the client directory')
def step_imp(context):
    original_path = Path('test\\files\\vid\\malyasia.avi')
    copied_path = Path(str(context.src_path)+'\\malyasia.avi')
    shutil.copy(original_path, copied_path)
    time.sleep(1)


@when(u'A .mov file is saved in the client directory')
def step_imp(context):
    original_path = Path('test\\files\\vid\\malyasia.mov')
    copied_path = Path(str(context.src_path)+'\\malyasia.mov')
    shutil.copy(original_path, copied_path)
    time.sleep(1)


@when(u'A .jpg file is saved in the client directory')
def step_imp(context):
    original_path = Path('test\\files\\img\\mountain.jpg')
    copied_path = Path(str(context.src_path)+'\\mountain.jpg')
    shutil.copy(original_path, copied_path)
    time.sleep(1)


@when(u'A .tiff file is saved in the client directory')
def step_imp(context):
    original_path = Path('test\\files\\img\\mountain.tiff')
    copied_path = Path(str(context.src_path)+'\\mountain.tiff')
    shutil.copy(original_path, copied_path)
    time.sleep(1)


@when(u'A .png file is saved in the client directory')
def step_imp(context):
    original_path = Path('test\\files\\img\\mountain.png')
    copied_path = Path(str(context.src_path)+'\\mountain.png')
    shutil.copy(original_path, copied_path)
    time.sleep(1)


@when(u'A .mp3 file is saved in the client directory')
def step_imp(context):
    original_path = Path('test\\files\\audio\\music.mp3')
    copied_path = Path(str(context.src_path)+'\\music.mp3')
    shutil.copy(original_path, copied_path)
    time.sleep(1)


@when(u'A .wav file is saved in the client directory')
def step_imp(context):
    original_path = Path('test\\files\\audio\\music.wav')
    copied_path = Path(str(context.src_path)+'\\music.wav')
    shutil.copy(original_path, copied_path)
    time.sleep(1)


@when(u'A .pdf file is saved in the client directory')
def step_imp(context):
    original_path = Path('test\\files\\misc\\hello.pdf')
    copied_path = Path(str(context.src_path)+'\\hello.pdf')
    shutil.copy(original_path, copied_path)
    time.sleep(1)


@when(u'A .docx file is saved in the client directory')
def step_imp(context):
    original_path = Path('test\\files\\misc\\word.docx')
    copied_path = Path(str(context.src_path)+'\\word.docx')
    shutil.copy(original_path, copied_path)
    time.sleep(1)


@when(u'A .xlsx file is saved in the client directory')
def step_imp(context):
    original_path = Path('test\\files\\misc\\excel.xlsx')
    copied_path = Path(str(context.src_path)+'\\excel.xlsx')
    shutil.copy(original_path, copied_path)
    time.sleep(1)
