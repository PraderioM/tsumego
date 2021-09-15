import os
from math import sqrt
from typing import Dict, Optional, Union
import json


class DefaultHandler:
    DEFAULT_VALUES_PATH = './cookies.json'
    HEIGHT_TO_WIDTH_RATIO = (1 + sqrt(5)) / 2

    @classmethod
    def from_json(cls, json_data: Dict[str, Union[int, None, str, bool]]):
        return DefaultHandler(tsumego_path=json_data['tsumego_path'],
                              first_page=json_data['first_page'],
                              width=json_data['width'],
                              height=json_data['height'],
                              stone_size=json_data['stone_size'],
                              show_fairy_lights=json_data['show_fairy_lights'],
                              join_tsumego_images=json_data['join_tsumego_images'],
                              n_joined_images=json_data['n_joined_images'])

    def __init__(self, tsumego_path: Optional[str] = None,
                 first_page: int = 1,
                 width: int = 720,
                 height: Optional[int] = None,
                 stone_size: int = 28,
                 show_fairy_lights: bool = False,
                 join_tsumego_images: bool = True,
                 n_joined_images: int = 6):
        self.default_path = tsumego_path
        self.first_page = first_page
        self.width = width
        self._height = height
        self.stone_size = stone_size
        self.show_fairy_lights = show_fairy_lights
        self.join_tsumego_images = join_tsumego_images
        self.n_joined_images = n_joined_images

    def to_json(self) -> Dict[str, Union[int, None, str, bool]]:
        return {
            'tsumego_path': self.default_path,
            'first_page': self.first_page,
            'width': self.width,
            'height': self._height,
            'stone_size': self.stone_size,
            'show_fairy_lights': self.show_fairy_lights,
            'join_tsumego_images': self.join_tsumego_images,
            'n_joined_images': self.n_joined_images
        }

    @property
    def height(self) -> int:
        if self._height is None:
            return int(DefaultHandler.HEIGHT_TO_WIDTH_RATIO * self.width)
        else:
            return self._height


def get_defaults() -> DefaultHandler:
    if os.path.exists(DefaultHandler.DEFAULT_VALUES_PATH):
        with open(DefaultHandler.DEFAULT_VALUES_PATH) as data_path:
            default_data = json.load(data_path)
            return DefaultHandler.from_json(default_data)
    else:
        return DefaultHandler()


def store_defaults(tsumego_path: Optional[str] = None,
                   first_page: int = 1,
                   width: int = 720,
                   height: Optional[int] = None,
                   stone_size: int = 28,
                   show_fairy_lights: bool = False,
                   join_tsumego_images: bool = True,
                   n_joined_images: int = 6):
    default_values = DefaultHandler(tsumego_path=tsumego_path, first_page=first_page,
                                    width=width, height=height, stone_size=stone_size,
                                    show_fairy_lights=show_fairy_lights,
                                    join_tsumego_images=join_tsumego_images, n_joined_images=n_joined_images)
    with open(DefaultHandler.DEFAULT_VALUES_PATH, 'w') as data_path:
        json.dump(default_values.to_json(), data_path)
