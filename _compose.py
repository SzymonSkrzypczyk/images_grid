from pathlib import Path
from typing import Iterable, Tuple, Union
from threading import Thread
from queue import Queue
from PIL import Image

N = 4
SIZE = 400, 400


def _resize_images(_images: Iterable[Image], size: Tuple[int, int], images: Queue):
    for i in _images:
        i = i.resize(size)
        images.put(i)


def compose(directory: Union[str, Path], size: Tuple[int, int], recursive: bool = False):
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        raise IsADirectoryError('You have to provide a valid directory!') from None
    images = Queue()
    if recursive:
        files = [i for i in directory.rglob('*.*') if i.suffix in ['.jpg', '.png']]
    else:
        files = [i for i in directory.iterdir() if i.suffix in ['.jpg', '.png']]
    num_cols = int(len(files) ** (1 / 2))
    width = size[0] * num_cols
    height = (len(files) % 3 + len(files) // 3) * size[1]
    current_y = 0
    new_img = Image.new('RGBA', (width, height))
    threads = []

    for i in range(0, len(files), N):
        th = Thread(target=_resize_images, args=(files[i:i + N], size, images))
        th.start()
        threads.append(th)
    for th in threads:
        th.join()

    while not images.empty():
        for i in range(0, width, size[1]):
            if images.empty():
                break
            new_img.paste(images.get(), (i, current_y))
        current_y += size[0]
    new_img.show()
    return new_img


if __name__ == '__main__':
    pass
