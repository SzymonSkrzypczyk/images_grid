from typing import Tuple
import typer
from _compose import compose

N = 4
SIZE = 400, 400
app = typer.Typer()


@app.command()
def create(directory: str, size: Tuple[int, int], recursive: bool = False, target: str = None):
    image = compose(directory, size, recursive)
    if target is not None:
        image.save(str(target))
    else:
        image.show()


if __name__ == '__main__':
    app()
