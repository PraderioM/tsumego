from glob import glob
import os
from random import randint
from typing import Optional, Tuple

import cv2
import numpy as np
from pdf2image import convert_from_path

from constants import WINDOW_NAME
from models import Manager
from store_results import store_results


def solve_tsumego(tsumego_path: str, first_page: int, out_dir: str, h: int, w: int, r: int):
    # Setup.
    current_page = first_page
    print_instructions()

    # Initialize window.
    manager = Manager(tsumego=np.zeros([10, 10, 3]), show_height=h, show_width=w, stone_size=r)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_GUI_NORMAL + cv2.WINDOW_AUTOSIZE)
    set_mouse_callbacks(manager=manager)

    while True:
        # Read pdf and get corresponding page from it.
        pages = convert_from_path(tsumego_path, first_page=current_page, last_page=current_page)
        if len(pages) == 0:
            print('Last pdf page has been reached.')
            break

        tsumego_page = np.array(pages[0])
        manager.reset(tsumego=tsumego_page)

        # Get path to where solutions will be stored.
        all_solved_tsumegos = glob(os.path.join(out_dir, '*'))
        out_path = os.path.join(out_dir, f'page_{current_page:03}.png')
        variation_number = 1
        while out_path in all_solved_tsumegos:
            out_path = os.path.join(out_dir, f'page_{current_page:03}_variation_{variation_number}.png')
            variation_number += 1

        # Solve tsumego page and store results.
        exit_editor = start_loop(manager=manager)
        store_results(tsumego=tsumego_page, path=out_path, solutions=manager.solutions, stone_size=r)

        # Go to the next page or exit program.
        if exit_editor:
            print('Goodbye. See you soon.')
            break

        current_page += 1

    cv2.destroyWindow(WINDOW_NAME)


def set_mouse_callbacks(manager: Manager):
    # Video mouse callbacks.
    def mouse_callback(event: int, x: int, y: int, flags: int, param: Optional):
        if event == cv2.EVENT_LBUTTONDOWN:
            stone = manager.get_new_stone(x, y)
            manager.add_stone(stone)
            manager.refresh = True

    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)


def start_loop(manager: Manager) -> bool:
    # Initialize images.
    image = manager.get_showed_image()

    # # Start fairy lights
    # fairy_lights_positions = get_fairy_lights_positions(image)
    # fairy_lights_semi_period = 1500
    # intensity = 0
    # direction = 1

    # Show images in a loop.
    while True:
        # Refresh video image if needed.
        if manager.refresh:
            image = manager.get_showed_image()
            manager.refresh = False

        # Show images and process key-board callbacks.
        # cv2.imshow(WINDOW_NAME, put_fairy_lights(image.copy(), positions=fairy_lights_positions,
        #                                          intensity=intensity,
        #                                          color=(20, 99, 156)))
        cv2.imshow(WINDOW_NAME, image)
        key = cv2.waitKey(1) & 0xFF

        # Process pressed key.
        break_loop, exit_editor = process_key(key=key, manager=manager)

        if break_loop:
            break

        # # Change fairy light intensity.
        # intensity += direction / fairy_lights_semi_period
        #
        # if intensity >= 1:
        #     intensity = 1
        #     direction = -1
        # elif intensity <= 0:
        #     intensity = 0
        #     direction = 1

    return exit_editor


def process_key(key: int, manager: Manager) -> Tuple[bool, bool]:
    break_loop = False
    exit_editor = False
    if key == ord('c'):
        manager.change_color()
        manager.refresh = True
    elif key == ord('p'):
        manager.reset_numbering()
        manager.refresh = True
    elif key == ord('b'):
        manager.remove_stone()
        manager.refresh = True
    elif key == ord('v'):
        manager.toggle_stone_visibility()
    elif key == ord('n'):
        break_loop = True
    elif key == ord('q'):
        break_loop = True
        exit_editor = True

    return break_loop, exit_editor


def print_instructions():
    print("""
KEYBOARD COMMANDS:
  `c`: Change color.
  `p`: Reset numbering.
  `b`: Remove last stone.
  `n`: Save current and go to next page.
  `q`: Save and quit tsumego.
  `v`: toggle stone visibility.
  `click`: Add new stone.
""")


def put_fairy_lights(image: np.ndarray,
                     positions: Tuple[Tuple[int, int], ...],
                     intensity: float = 1,
                     radius: int = 3,
                     color: Tuple[int, int, int] = (255, 255, 255)) -> np.ndarray:
    for cx, cy in positions:
        img_color = tuple(image[cy, cx].tolist())
        new_color = tuple([min(255, max(0, int(c1 * (1-intensity) + c2 * intensity)))
                           for c1, c2 in zip(img_color, color)])
        image = cv2.circle(image, center=(cx, cy), radius=radius, color=new_color, thickness=-1)

    return image


def get_fairy_lights_positions(image: np.ndarray,
                               min_n_lights: int = 100,
                               max_n_light: int = 201) -> Tuple[Tuple[int, int], ...]:
    n_fairy_lights = randint(min_n_lights, max_n_light)
    h, w, _ = image.shape

    positions = [(randint(0, w - 1), randint(0, h - 1)) for _ in range(n_fairy_lights)]

    return tuple(positions)
