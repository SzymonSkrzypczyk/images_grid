from queue import Queue
from threading import Thread
from typing import Union, Tuple
from pathlib import Path
from PIL import Image
import typer

N = 4
SIZE = 400, 400
images = Queue()
TEST = Path(__file__).parent.parent / 'images' / 'Normal'
app = typer.Typer()


def resize(imgs, size):
    for im in imgs:
        _im = Image.open(str(im))
        _im = _im.resize(size)
        images.put(_im)


def process(path: Union[str, Path], target: Union[str, Path], size: Tuple[int, int] = SIZE):
    path = Path(path)
    if not path.exists() or not path.is_dir():
        raise IsADirectoryError('You have to provide a valid directory!') from None
    images = Queue()
    files = [i for i in path.iterdir() if i.suffix in ['.jpg', '.png']]
    num_cols = int(len(files) ** (1/2))
    width = size[0] * num_cols
    height = (len(files) % 3 + len(files) // 3) * size[1]
    current_y = 0
    new_img = Image.new('RGBA', (width, height))
    threads = []

    for i in range(0, len(files), N):
        th = Thread(target=resize, args=(files[i:i+N], size))
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
    target = Path(target)
    target.touch(exist_ok=True)
    new_img.save(str(target))


@app.command()
def grid(path: str, target: str, size: Tuple[int, int]):
    process(path, target, size)


if __name__ == '__main__':
    app()