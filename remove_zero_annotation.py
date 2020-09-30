import sys
from pathlib import Path


def main():
    argv = sys.argv

    # 引数があれば引数, なければ入力
    path = argv[1] if len(argv) >= 2 \
        else input('> Enter path: ')
    path = Path(path)

    if not path.exists():
        print('存在しないパスが入力されました.')
        print('パスに￥が含まれる場合はクォーテーションで囲んでください.')
        exit(-1)

    if path.is_file():
        path = path.parent

    # convert path into absolute path
    target_path = path.resolve()

    # dirs[0]: 001, dirs[1]: Images / Labels
    dirs = []

    dirs.append(target_path.name)  # 001 / 002 ...
    target_path = target_path.parent
    dirs.append(target_path.name)  # Images / Labels
    target_path = target_path.parent

    # determine what specified path is 'Images' or 'Labels'
    if dirs[1] == 'Images':
        path = Path(target_path, 'Labels', dirs[0])

    p_img_base = Path(target_path, 'Images', dirs[0])

    # 削除するファイルのパス
    path_list = []
    exts = ['jpg', 'png', 'bmp', 'jpeg']

    for p_txt in path.glob('*'):
        # not .txt or directory -> continue
        if p_txt.suffix != '.txt' or p_txt.is_dir():
            continue

        # first element is not '0'
        if p_txt.read_text()[0] != '0':
            continue

        # convert path into relative path, and append
        p_txt = p_txt.relative_to(path.cwd())
        path_list.append(p_txt)

        for ext in exts:
            # image path
            p_img = p_img_base.joinpath(f'{p_txt.stem}.{ext}')

            if p_img.exists():
                # convert path into relative path, and append
                p_img = p_img.relative_to(path.cwd())
                path_list.append(p_img)

    # is not exist target files
    if len(path_list) == 0:
        print('\nThere is no zero annotation file.')
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

    # do not remove
    if not is_remove:
        print('Exit without removing.')
        exit()

    # ファイルが存在する事は確認済み
    for path in path_list:
        # remove
        path.unlink()
        print(f'removed: {path}')


if __name__ == '__main__':
    main()
