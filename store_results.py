from typing import List

import cv2
import numpy as np

from models import Stone


def store_results(tsumego: np.ndarray, path: str, solutions: List[Stone], stone_size: int = 10):
    out_tsumego = tsumego.copy()

    for stone in solutions:
        out_tsumego = stone.draw_on_image(img=out_tsumego, size=stone_size)

    cv2.imwrite(path, img=out_tsumego)
