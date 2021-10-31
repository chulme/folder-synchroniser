import server as srv
import client as cl
import argparse
import time


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
    parser.add_argument('src_path', type=str,
                        help='Path to a source directory,.')
    parser.add_argument('dst_path', type=str,
                        help='Path to a destination directory.')
    args = parser.parse_args()
    main(src_path=args.src_path, dst_path=args.dst_path)
    #main("test_client", "test_server")
