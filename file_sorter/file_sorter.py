from collections import defaultdict
import os
import shutil
import sys


ARCHIVE = 'archives'
AUDIO = 'audio'
DOC = 'documents'
IMG = 'images'
OTHER = 'other'
VID = 'videos'

EXTENSIONS = {
    '7z': ARCHIVE,
    'ai': IMG,
    'avi': VID,
    'bmp': IMG,
    'doc': DOC,
    'docx': DOC,
    'flac': AUDIO,
    'gif': IMG,
    'ico': IMG,
    'jpeg': IMG,
    'jpg': IMG,
    'mid': AUDIO,
    'midi': AUDIO,
    'mp3': AUDIO,
    'mp4': VID,
    'mpeg': VID,
    'mpg': VID,
    'odp': DOC,
    'odt': DOC,
    'ods': DOC,
    'ogg': AUDIO,
    'pdf': DOC,
    'png': IMG,
    'pps': DOC,
    'ppt': DOC,
    'pptx': DOC,
    'psd': IMG,
    'rar': ARCHIVE,
    'rtf': DOC,
    'svg': IMG,
    'tif': IMG,
    'tiff': IMG,
    'tga': IMG,
    'txt': DOC,
    'wav': AUDIO,
    'webm': VID,
    'webp': IMG,
    'wmv': VID,
    'xls': DOC,
    'xlsm': DOC,
    'xlsx': DOC,
    'zip': ARCHIVE
}

EXT_DICT = defaultdict(lambda: OTHER, EXTENSIONS)


def main():
    print(
        'Enter path to the folder you want to sort.\n'
        '(Example: c:\\downloads)'
    )
    source_folder = get_source()
    sort(source_folder)


# Custom functions.
def get_source() -> str:
    """Gets a folder path from user input and returns it."""

    source_folder = input('Path: ').strip()
    if not os.path.exists(source_folder):
        sys.exit('Path does not exist.')
    return source_folder


def sort(source_folder: str) -> None:
    """Moves all files from source folder into categorized subfolders."""

    files = os.listdir(source_folder)
    for file in files:
        current_file = os.path.join(source_folder, file)
        file_extension = os.path.splitext(file)[1][1:]
        file_category = EXT_DICT[file_extension]
        target_folder = os.path.join(source_folder, file_category)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        new_file = os.path.join(target_folder, file)
        try:
            shutil.move(current_file, new_file)
        except Exception as e:
            print(f'Error with file "{file}":', e)


if __name__ == '__main__':
    main()
