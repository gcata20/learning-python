from collections import defaultdict
import os
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
        'Enter path to the folder you want to sort.'
        '(Example: c:\\downloads)'
    )
    target = get_target()
    # result = sort(target)
    # print(result)


# Custom functions.
def get_target():
    target = input('Path: ').strip()
    if not os.path.exists(target):
        sys.exit('Path does not exist.')
    return target


def sort(target: str):
    ...


if __name__ == '__main__':
    main()
