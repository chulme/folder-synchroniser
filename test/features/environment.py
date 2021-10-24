from pathlib import Path
from behave import given, when, then
import shutil


def before_all(context):
    build_path = Path('test\\build')
    print(build_path.resolve())
    if build_path.exists():
        shutil.rmtree(build_path)
    build_path.mkdir(parents=True, exist_ok=False)
    print("Created build directory.")
