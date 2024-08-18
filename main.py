import pathlib
import random
import string
import uuid
from typing import Annotated, Optional

import typer


app = typer.Typer(pretty_exceptions_enable=False)


def resolve_path(path: pathlib.Path) -> pathlib.Path:
    return path.resolve()


@app.command(name="create")
def files(
    number: Annotated[int, typer.Option()],
    directory: Annotated[Optional[pathlib.Path], typer.Option(callback=resolve_path)] = pathlib.Path(__file__).parents[
        0
    ],
    text: Annotated[bool, typer.Option()] = True,
):
    # current_dir
    files = [directory / f"{str(uuid.uuid4())[:5]}.dummy" for _ in range(number)]

    for file in files:
        if text:
            content = "\n".join("".join(random.choices(string.ascii_letters, k=20)) for _ in range(5))
            file.write_text(content)
        else:
            file.touch()


@app.command(name="edit")
def edit_files(
    directory: Annotated[Optional[pathlib.Path], typer.Option(callback=resolve_path)] = pathlib.Path(__file__).parents[
        0
    ],
):
    files = list(directory.glob("*.dummy"))
    for file in files:
        content = "\n".join("".join(random.choices(string.ascii_letters, k=20)) for _ in range(5))
        file.write_text(content)


@app.command(name="delete")
def delete_files(
    number: Annotated[int, typer.Option()],
    directory: Annotated[Optional[pathlib.Path], typer.Option(callback=resolve_path)] = pathlib.Path(__file__).parents[
        0
    ],
):
    files = list(directory.glob("*.dummy"))
    for i in range(min(number, len(files))):
        files[i].unlink()


if __name__ == "__main__":
    app()
