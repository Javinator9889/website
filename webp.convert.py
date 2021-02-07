import os
import subprocess
from glob import glob, iglob
from pathlib import Path
from pprint import pprint
from typing import FrozenSet, Dict


def find_all(types: set = { '*.png', '*jpg' }, directory: str = "public/images") -> FrozenSet[Path]:
    files = set()
    for file_type in types:
        files.update({Path(src) for src in glob(f"{directory}/**/{file_type}", recursive=True)})

    return files


def convert_to_webp(files: FrozenSet[Path], options: FrozenSet[str] = { '-mt', '-m 6', '-z 9' }) -> FrozenSet[Path]:
    webp_files = {}
    command = f"cwebp {' '.join(options)}"
    command = command + " {0} -o {1}"
    for file in files:
        target = file.with_suffix('.webp')
        proc = subprocess.run(command.format(file, target).split())
        if proc.returncode != 0:
            print(f"Error while moving {file} to {target}")
        else:
            webp_files[file] = target
    
    return webp_files


def use_webp_files(files_map: Dict[Path, Path], directory: str = "public"):
    files_map = { source.name: webp.name for source, webp in files_map.items() }
    for file in iglob(f"{directory}/**/*.html", recursive=True):
        print(f"Replacing pictures in {file}...")
        with open(file, 'r') as html_file:
            contents = html_file.read()
        for source, webp in files_map.items():
            contents = contents.replace(source, webp)
        with open(file, 'w') as html_file:
            html_file.write(contents)


def delete_old_files(files: FrozenSet[Path]):
    for file in files:
        file.unlink()


files = find_all()
pprint(files)
webp_files = convert_to_webp(files)
pprint(webp_files)
use_webp_files(webp_files)
delete_old_files(files)
