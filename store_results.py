from glob import glob
import os
from typing import List

import cv2
import numpy as np

from models import Stone
from join_images import join_images


def store_results(tsumego: np.ndarray, path: str, solutions: List[Stone], stone_size: int = 10):
    out_tsumego = tsumego.copy()

    for stone in solutions:
        out_tsumego = stone.draw_on_image(img=out_tsumego, size=stone_size)

    cv2.imwrite(path, img=out_tsumego)


def store_joint_images(first_page: int, last_page: int, out_dir: str, n: int = 6):
    image_path_list: List[str] = []
    all_tsumego = list(glob(os.path.join(out_dir, '*')))
    is_variation_decided = False
    variation = 0
    for page in range(first_page, last_page + 1):
        image_path = get_out_image_name(out_dir=out_dir, page=page, variation=variation)

        if not is_variation_decided:
            while image_path in all_tsumego:
                variation += 1
                image_path = get_out_image_name(out_dir=out_dir, page=page, variation=variation)
            variation -= 1
            image_path = get_out_image_name(out_dir=out_dir, page=page, variation=variation)

        if variation == -1:
            continue
        else:
            if image_path in all_tsumego:
                is_variation_decided = True
            else:
                continue

        image_path = get_out_image_name(out_dir=out_dir, page=page, variation=variation)
        image_path_list.append(image_path)

    while len(image_path_list) > 0:
        image_batch = image_path_list[:n]
        image_path_list = image_path_list[n:]
        joined_image = join_images(image_path_list=image_batch)

        out_path = get_joined_image_name(out_dir=out_dir)
        cv2.imwrite(out_path, joined_image)


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
