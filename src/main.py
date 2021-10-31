import server as srv
import client as cl
import argparse
import time
from pathlib import Path


def main(src_path: str, dst_path: str):

    components = [srv.Server(dst_path), cl.Client(src_path)]

    for c in components:
        c.start()

    is_running = True
    while is_running:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            is_running = False

    for c in components:
        c.terminate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="some desc")
    parser.add_argument('--src', type=Path,
                        help='Path to a source directory,.')
    parser.add_argument('--dst', type=Path,
                        help='Path to a destination directory.')
    args = parser.parse_args()
    if Path(args.src).is_dir() and Path(args.dst).is_dir():
        main(src_path=args.src, dst_path=args.dst)
    else:
        raise parser.error(
            message=f'A provided path is not recognised as a directory.\n\n \
            Please ensure the following paths are correct:\n\t \
                {args.src.resolve()}\n\t{args.dst.resolve()}')
