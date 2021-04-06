#!/bin/python
# coding: utf-8

from PIL import Image
from pathlib import Path
from typing import List, Optional, Union
from zipfile import ZipFile
import os
import re
import shutil
import tempfile

_ImagePattern = re.compile(r'''\.(?:jpe?g|png|gif)$''', re.IGNORECASE)


def file_keys(name: str) -> List[Union[str, int]]:
    result: List[Union[str, int]] = []
    for it in re.findall(r'''\d+|\D+''', name):
        if it[0] in '0123456789':
            result.append(int(it))
        else:
            result.append(it)
    return result


def is_image(name: str) -> bool:
    return _ImagePattern.search(name) is not None


class App:
    def __init__(self) -> None:
        self.work_dir = tempfile.TemporaryDirectory()

    def generate(self, filepath: str, output: Optional[str]=None) -> None:
        zf = ZipFile(filepath)
        first = sorted(filter(is_image, zf.namelist()), key=file_keys)[0]

        _output: Path
        if output is None:
            _output = Path(filepath).with_suffix('.jpg')
        else:
            _output = Path(output)

        zf.extract(first, self.work_dir.name)
        original_image_file = os.path.join(self.work_dir.name, first)

        image = Image.open(original_image_file)
        image.thumbnail((2000, 2000), Image.LANCZOS)
        image.save(str(_output), format='jpeg')

        return


if __name__ == '__main__':
    import fire
    fire.Fire(App)
