import subprocess
from glob import iglob
from pathlib import Path
from typing import FrozenSet, Dict


def find_all(types: set = {'*.png', '*jpg'}, directory: str = "public/images") -> FrozenSet[Path]:
    files = set()
    for file_type in types:
        files.update({Path(src)
                      for src in iglob(f"{directory}/**/{file_type}", recursive=True)})

    return files


def convert_to_webp(files: FrozenSet[Path], 
                    options: FrozenSet[str] = {'-mt', '-m 6', '-q 75', '-alpha_q 100', '-af', '-pass 10', '-v'},
                    ignored_files: FrozenSet[str] = {'view-on-github', 'telegram-button'}) -> FrozenSet[Path]:
    webp_files = {}
    lossless_cmd = "cwebp -mt -lossless -z 9 -af -pass 10 -v {0} -o {1}"
    command = f"cwebp {' '.join(options)}"
    command = command + " {0} -o {1}"
    for file in files:
        target = file.with_suffix('.webp')
        if any(file.name.startswith(ignored) for ignored in ignored_files):
            cmd = lossless_cmd
            print(f"> Ignoring file {file.name} (lossless compression)", end='\n\n')
        else:
            cmd = command
        proc = subprocess.run(cmd.format(file, target).split())
        if proc.returncode != 0:
            print(f"Error while moving {file} to {target}")
        else:
            webp_files[file] = target

    return webp_files


def use_webp_files(files_map: Dict[Path, Path], directory: str = "public"):
    files_map = {source.name: webp.name for source, webp in files_map.items()}
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


print("> Looking for all images in public/", end="\n\n")
files = find_all()

print(f"> Converting all found files ({len(files)}) to WebP...", end="\n\n")
webp_files = convert_to_webp(files)

print("> Using WebP images instead of PNG or JPG...", end="\n\n")
use_webp_files(webp_files)

print("> Removing old images to save space...", end="\n\n")
delete_old_files(files)

print("> Operation completed! Exiting...")
exit(0)
