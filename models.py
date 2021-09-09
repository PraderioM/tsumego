import cv2
import numpy as np

from typing import List


class Stone:
    def __init__(self, x: float, y: float, number: int, black: True, visible: bool = True):
        self._x = x
        self._y = y
        self._number = number
        self._black = black
        self._visible = visible

    def draw_on_image(self, img: np.ndarray, size: int,
                      font_face: int = 1, font_scale: int = 2,
                      thickness: int = 2) -> np.ndarray:
        img_h, img_w, _ = img.shape
        cx = int(self._x * img_w)
        cy = int(self._y * img_h)
        if self._black:
            color = (0, 0, 0)
            text_color = (255, 255, 255)
        else:
            color = (255, 255, 255)
            text_color = (0, 0, 0)

        if self._visible:
            img = cv2.circle(img=img, center=(cx, cy), radius=size, color=color, thickness=-1)
        img = cv2.circle(img=img, center=(cx, cy), radius=size, color=text_color, thickness=1)
        number = str(self._number)
        (x_shift, y_shift), _ = cv2.getTextSize(number, fontFace=font_face, fontScale=font_scale, thickness=thickness)
        org = int(cx - x_shift / 2), int(cy + y_shift / 2)

        return cv2.putText(img, text=str(self._number), org=org,
                           fontFace=font_face, fontScale=font_scale,
                           color=text_color, thickness=thickness)

    @property
    def is_black(self) -> bool:
        return self._black

    @property
    def number(self) -> int:
        return self._number

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y


class Manager:
    FIRST_STONE_NUMBER = 1
    FIRST_STONE_BLACK = True
    DEFAULT_VISIBLE_STATE = True

    def __init__(self, tsumego: np.ndarray, show_height: int, show_width: int, stone_size: int):
        self._solutions: List[Stone] = []
        self.refresh = False
        self._stone_size = stone_size
        self._show_height = show_height
        self._show_width = show_width
        self._current_number = self.FIRST_STONE_NUMBER
        self._current_black = self.FIRST_STONE_BLACK
        self._tsumego = tsumego
        self._stone_visible = self.DEFAULT_VISIBLE_STATE

    def reset(self, tsumego: np.ndarray):
        self._solutions: List[Stone] = []
        self.refresh = False
        self._current_number = self.FIRST_STONE_NUMBER
        self._current_black = self.FIRST_STONE_BLACK
        self._stone_visible = self.DEFAULT_VISIBLE_STATE
        self.tsumego = tsumego

    def add_stone(self, stone: Stone):
        self._solutions.append(stone)
        self._current_black = not self._current_black
        self._current_number += 1

    def remove_stone(self):
        if len(self._solutions) > 0:
            self._solutions.pop()
            if len(self._solutions) == 0:
                self._current_black = self.FIRST_STONE_BLACK
                self._current_number = self.FIRST_STONE_NUMBER
            else:
                self._current_black = not self._solutions[-1].is_black
                self._current_number = self._solutions[-1].number + 1

    def reset_numbering(self):
        self._current_black = self.FIRST_STONE_BLACK
        self._current_number = self.FIRST_STONE_NUMBER
        self._stone_visible = self.DEFAULT_VISIBLE_STATE

    def change_color(self):
        self._current_black = not self._current_black

    def get_new_stone(self, x: int, y: int) -> Stone:
        x = x / self._show_width
        y = y / self._show_height

        if len(self._solutions) != 0 and self._current_number != self.FIRST_STONE_NUMBER:
            h, w, _ = self._tsumego.shape
            diameter = 2 * self._stone_size
            prev_x = self._solutions[-1].x
            prev_y = self._solutions[-1].y
            x_diff = diameter * int(round((x - prev_x) * w / diameter)) / w
            y_diff = diameter * int(round((y - prev_y) * h / diameter)) / h
            x = prev_x + x_diff
            y = prev_y + y_diff

        return Stone(x=x, y=y, number=self._current_number, black=self._current_black, visible=self._stone_visible)

    def get_showed_image(self):
        showed_image = self._tsumego.copy()
        for stone in self._solutions:
            showed_image = stone.draw_on_image(img=showed_image, size=self._stone_size)
        return cv2.resize(showed_image, (self._show_width, self._show_height))

    @property
    def tsumego(self):
        return self._tsumego.copy()

    @tsumego.setter
    def tsumego(self, img: np.ndarray):
        self._tsumego = img.copy()
        self.refresh = True

    @property
    def solutions(self) -> List[Stone]:
        return self._solutions[:]

    def toggle_stone_visibility(self):
        self._stone_visible = not self._stone_visible
