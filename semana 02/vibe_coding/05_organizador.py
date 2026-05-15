#!/usr/bin/env python3
import os
import shutil
from pathlib import Path


EXTENSION_MAP = {
    'imagens': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'},
    'docs': {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md', '.rtf'},
    'audio': {'.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a'},
    'video': {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'},
}


def get_category(extension: str) -> str:
    extension = extension.lower()
    for category, extensions in EXTENSION_MAP.items():
        if extension in extensions:
            return category
    return 'outros'


def organize_folder(folder: Path) -> None:
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f'O diretório não existe: {folder}')

    counts = {}
    for item in folder.iterdir():
        if item.is_dir():
            continue
        category = get_category(item.suffix)
        target_dir = folder / category
        target_dir.mkdir(exist_ok=True)
        destination = target_dir / item.name
        shutil.move(str(item), str(destination))
        counts[category] = counts.get(category, 0) + 1
        print(f'Movendo: {item.name} -> {category}/')

    if counts:
        print('\nResumo de arquivos movidos por categoria:')
        for category, total in sorted(counts.items()):
            print(f'  {category}: {total}')
    else:
        print('\nNenhum arquivo encontrado para mover.')


def main() -> None:
    current_folder = Path.cwd()
    print(f'Organizando arquivos em: {current_folder}')
    organize_folder(current_folder)
    print('Organização concluída.')


if __name__ == '__main__':
    main()
