import argparse

common_arguments = argparse.ArgumentParser(add_help=False)
common_arguments.add_argument('--ip', type=str, required=True, help='IP address')
common_arguments.add_argument('--port', type=int, default=54321, help='port')
common_arguments.add_argument('--width', type=int, default=110, help='width of the display')
common_arguments.add_argument('--height', type=int, default=9, help='height of the display')
