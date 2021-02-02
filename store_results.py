from glob import glob
import os
from typing import List, Optional

import cv2
import numpy as np

from models import Stone


def store_results(tsumego: np.ndarray, path: str, solutions: List[Stone], stone_size: int = 10):
    out_tsumego = tsumego.copy()

    for stone in solutions:
        out_tsumego = stone.draw_on_image(img=out_tsumego, size=stone_size)

    cv2.imwrite(path, img=out_tsumego)


def join_images(first_page: int, last_page: int, out_dir: str):
    image_path_list: List[str] = []
    all_tsumego = list(glob(os.path.join(out_dir, '*')))
    for page in range(first_page, last_page + 1):
        variation = 0
        image_path = get_out_image_name(out_dir=out_dir, page=page, variation=variation)
        while image_path in all_tsumego:
            variation += 1
            image_path = get_out_image_name(out_dir=out_dir, page=page, variation=variation)

        if variation == 0:
            continue

        image_path = get_out_image_name(out_dir=out_dir, page=page, variation=variation - 1)
        image_path_list.append(image_path)

    joined_image: Optional[np.ndarray] = None
    h: Optional[int] = None
    w: Optional[int] = None
    for image_path in image_path_list:
        image = cv2.imread(image_path)
        if h is None or w is None:
            h, w, _ = image.shape
        image = cv2.resize(image, (w, h))

        if joined_image is None:
            joined_image = image
        else:
            joined_image = np.concatenate([joined_image, image], axis=0)


def get_out_image_name(out_dir: str, page: int, variation: int = 0) -> str:
    if variation == 0:
        return os.path.join(out_dir, f'page_{page:03}.png')
    else:
        return os.path.join(out_dir, f'page_{page:03}_variation_{variation}.png')


def get_joined_image_name(out_dir: str) -> str:
    joined_image_name = os.path.join(out_dir, f'joined_tsumego.png')
    all_tsumego = list(glob(os.path.join(out_dir, '*')))
    i = 1
    while joined_image_name in all_tsumego:
        joined_image_name = os.path.join(out_dir, f'joined_tsumego_{i:03}.png')
        i += 1
    return joined_image_name
