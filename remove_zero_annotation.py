import sys
from pathlib import Path


def main():
    argv = sys.argv

    # 引数があれば引数, なければ入力
    path = argv[1] if len(argv) >= 2 \
        else input('> Enter path: ')
    path = Path(path)

    if not path.exists():
        print('存在しないディレクトリが入力されました.')
        print('パスに￥が含まれる場合はクォーテーションで囲んでください.')
        sys.exit(-1)

    if path.is_file():
        path = Path(path.parent)

    # convert path into absolute path
    target_path = path.resolve()

    # dirs[0]: 001, dirs[1]: Images / Labels
    dirs = []

    dirs.append(target_path.stem)
    target_path = Path(target_path.parent)
    dirs.append(target_path.stem)
    target_path = Path(target_path.parent)

    # determine what specified path is 'Images' or 'Labels'
    if dirs[1] == 'Images':
        p = Path()

        add = [path.parents[1], 'Labels', dirs[0]]
        path = p.joinpath(*add)

    # 削除するファイルのパス
    path_list = []

    for file in path.glob('*'):
        p_txt = Path(file)

        # not .txt or directory -> continue
        if p_txt.suffix != '.txt' or p_txt.is_dir():
            continue

        # first element is '0'
        if p_txt.read_text()[0] != '0':
            continue

        add = ['Images', dirs[0], p_txt.name]
        p_img = target_path.joinpath(*add)

        # change extension .* -> .jpg
        p_img = p_img.with_suffix('.jpg')

        # convert path into relative path
        p_img = p_img.relative_to(path.cwd())

        # append
        path_list.append(p_txt)
        if p_img.exists():
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
        print(f'deleted: {path}')


if __name__ == '__main__':
    main()
