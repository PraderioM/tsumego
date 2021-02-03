from math import sqrt, ceil
from typing import List, Optional

import cv2
import numpy as np


def join_images(image_path_list: List[str]):
    h: Optional[int] = None
    w: Optional[int] = None
    n = len(image_path_list)
    n_cols = int(ceil(sqrt(n)))

    joined_image: Optional[np.ndarray] = None
    while len(image_path_list) > 0:
        row = image_path_list[:n_cols]
        image_path_list = image_path_list[n_cols:]
        row_image = None
        while len(row) > 0:
            image_path = row.pop(0)
            image = cv2.imread(image_path)
            if h is None or w is None:
                h, w, _ = image.shape
            image = cv2.resize(image, (w, h))
            if row_image is None:
                row_image = image
            else:
                row_image = np.concatenate([row_image, image], axis=1)

        n_missing = n_cols * w - row_image.shape[1]
        if n_missing > 0 and joined_image is not None:
            empty_image = np.zeros(shape=(h, n_missing, 3), dtype=np.uint8)
            row_image = np.concatenate([row_image, empty_image], axis=1)

        if joined_image is None:
            joined_image = row_image
        else:
            joined_image = np.concatenate([joined_image, row_image], axis=0)

    return joined_image
