import os
from typing import Optional, Tuple

import cv2
import numpy as np

NO_ANSWERS = ('n', 'no', 'nope')
YES_ANSWERS = ('y', 'yes', 'yep')


def get_tsumego() -> Tuple[np.ndarray, str]:
    while True:
        tsumego_path = input('Insert path to tsumego image:\n\t')
        tsumego_path = os.path.abspath(tsumego_path)
        if not os.path.exists(tsumego_path):
            print(f'There is no file with location `{tsumego_path}`.')
        else:
            img = cv2.imread(tsumego_path)
            if img is None or img.size == 0:
                print(f'Could not read image located at `{tsumego_path}`.')
            else:
                return img, tsumego_path

        print('Please insert a valid path.')


def get_solved_tsumego_path(in_tsumego_path: Optional[str] = None) -> str:
    ask_message = 'Insert solved tsumego path'
    # Get default.
    if in_tsumego_path is None:
        default_out_path = ''
    else:
        split_video_path = list(os.path.splitext(in_tsumego_path))
        if len(split_video_path) <= 1:
            default_out_path = ''
        else:
            split_video_path[-1] = 'png'
            split_video_path[-2] = split_video_path[-2] + '_solved'
            default_out_path = '.'.join(split_video_path)

    # Ask user for input.
    while True:
        if len(default_out_path) == 0:
            out_path = input(f'{ask_message}:\n\t')
        else:
            out_path = input(f'{ask_message}: [{default_out_path}]\n\t')
        if len(out_path) == 0:
            out_path = default_out_path
        out_path = os.path.abspath(out_path)
        if os.path.exists(out_path):
            while True:
                proceed = input(f'There already exists a file with location `{out_path}`.\n'
                                f'Are you sure you want to proceed? If you do previous file will be removed: [y/N]')
                if proceed.lower() in list(NO_ANSWERS) + ['']:
                    break
                elif proceed.lower() in YES_ANSWERS:
                    return out_path
                else:
                    print(f"I don't understand your answer. Please repeat it.")
            continue
        else:
            out_path = _optionally_create_directory(out_path)
            if out_path is None:
                print('Please insert a valid path.')
                continue
            else:
                return out_path


def get_size(size_name: str, default_val: int = 768) -> int:
    while True:
        size_string = input(f'Insert {size_name}: [{default_val}]\n\t')

        if len(size_string) == 0:
            return default_val

        if not size_string.isnumeric():
            print('Please insert a valid integer.')
        else:
            return int(size_string)


def _optionally_create_directory(path: str) -> Optional[str]:
    if not os.path.exists(os.path.dirname(path)):
        while True:
            proceed = input(
                f'There exists no directory named `{os.path.dirname(path)}`. Do you want me to create it?: [Y/n]')
            if proceed.lower() in NO_ANSWERS:
                break
            elif proceed.lower() in list(YES_ANSWERS) + ['']:
                os.makedirs(os.path.dirname(path))
                return path
            else:
                print(f"I don't understand your answer. Please repeat it.")
        return None
    else:
        return path
