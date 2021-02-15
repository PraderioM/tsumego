import os
from typing import Optional

from pdf2image import convert_from_path

NO_ANSWERS = ('n', 'no', 'nope')
YES_ANSWERS = ('y', 'yes', 'yep')


def get_tsumego() -> str:
    while True:
        tsumego_path = input('Insert path to tsumego pdf:\n\t')
        tsumego_path = os.path.abspath(tsumego_path)
        if not os.path.exists(tsumego_path):
            print(f'There is no file with location `{tsumego_path}`.')
        else:
            try:
                pages = convert_from_path(tsumego_path, first_page=1, last_page=1)
            except:
                pages = []

            if len(pages) == 0:
                print(f'Could not read pdf located at `{tsumego_path}`.')
            else:
                return tsumego_path

        print('Please insert a valid path.')


def get_solved_tsumego_dir(tsumego_path: Optional[str] = None) -> str:
    ask_message = 'Insert directory where solved tsumego will be stored'
    # Get default.
    if tsumego_path is None:
        default_out_dir = ''
    else:
        split_video_path = list(os.path.splitext(tsumego_path))
        if len(split_video_path) <= 1:
            default_out_dir = ''
        else:
            split_video_path = split_video_path[:-1]
            split_video_path[-1] = split_video_path[-1] + '_solutions'
            default_out_dir = '.'.join(split_video_path)

    # Ask user for input.
    if len(default_out_dir) == 0:
        out_dir = input(f'{ask_message}:\n\t')
    else:
        out_dir = input(f'{ask_message}: [{default_out_dir}]\n\t')
    if len(out_dir) == 0:
        out_dir = default_out_dir
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def get_positive_integer(size_name: str, default_val: int = 768) -> int:
    while True:
        size_string = input(f'Insert {size_name}: [{default_val}]\n\t')

        if len(size_string) == 0:
            return default_val

        if not size_string.isnumeric():
            print('Please insert a valid integer.')
        else:
            return max(1, int(size_string))


def get_bool(message: str, default: bool) -> bool:
    if default:
        message = message + ' [Y/n]\n\t'
    else:
        message = message + ' [y/N]\n\t'

    while True:
        response = input(message)

        if len(response) == 0:
            return default

        response = response.lower()
        if response in YES_ANSWERS:
            return True
        elif response in NO_ANSWERS:
            return False
        else:
            print('I do not understand please repeat your answer.')
