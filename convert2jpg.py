import ffmpeg
from pathlib import Path


def convert_extension(path, ext):
    input_path = Path(path)

    # not exist
    if not input_path.exists():
        return -1

    # .* -> .jpg
    output_path = input_path.with_suffix(ext)
    out = str(output_path)

    # high compress
    (
        ffmpeg
        .input(path)
        .output(
            out,
            qmin='1',
            q='1',
            loglevel='fatal')
        .run()
    )

    return 0


if __name__ == "__main__":
    import sys
    argv = sys.argv
    if len(argv) < 2:
        print('  Need a directory path included images.\n')

        print('Usage:')
        print('  * python convert2jpg.py <directory path>\n')

        print('Example:')
        print('  * python convert2jpg.py datasets/Images/001/')
        exit(-1)

    target_ext = '.jpg'

    encode_exts = [
        '.png', '.PNG',
        '.gif', '.GIF',
        '.tif', '.TIF',
        '.tiff', '.TIFF'
    ]
    no_encode_exts = [
        '.jpeg', 'JPEG',
        '.JPG'
    ]

    path_list = []

    dir_path = Path(argv[1])
    if not dir_path.exists():
        print('  This directory is not exist.')

    imgs = dir_path.glob('*')
    for i, img in enumerate(imgs):
        print(f'\r{i}', end='')

        p = Path(img)

        if p.is_dir():
            continue

        name = p.stem
        ext = p.suffix

        # equal to target extension
        if ext == target_ext:
            continue

        # no encode
        if ext in no_encode_exts:
            out = Path(p.parent)
            out.joinpath(f'{name}{target_ext}')
            # rename
            p.rename(out)
            continue

        # encode
        if ext in encode_exts:
            # convert
            # st = convert_extension(str(p), target_ext)

            # # success
            # if st == 0:
            #     path_list.append(p)
            pass

    # is not exist target files
    if len(path_list) == 0:
        print('\nThere is no encoded file.')
        exit()

    # show list 10 num
    for i, path in enumerate(path_list):
        print(path)
        if i == 9:
            print('  ...')
            break
    print()

    # check remove OK?
    ans_list = ['y', 'Y', 'yes', 'Yes', 'YES']
    ans = input('Remove OK? (y/N): ')

    # true / false
    is_remove = ans in ans_list

    for path in path_list:
        path.unlink()
        print(f'deleted: {path}')
