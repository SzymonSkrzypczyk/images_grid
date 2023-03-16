from pathlib import Path
from typing import Iterable, Tuple, Union
from queue import Queue
from PIL import Image

N = 4
SIZE = 400, 400
IMAGES = Queue()


def _resize_images(_images: Iterable[Image], size: Tuple[int, int]):
    for i in _images:
        i = i.resize(size)
        IMAGES.put(i)


def compose(directory: Union[str, Path], size: Tuple[int, int]):
    ...


if __name__ == '__main__':
    pass
