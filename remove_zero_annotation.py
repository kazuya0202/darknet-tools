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
        tmp_path = Path(path.parent).parent
        path = tmp_path.joinpath(f'Labels/{dirs[0]}')

    # 削除するファイルのパス
    path_list = []

    for file in path.glob('*'):
        p_txt = Path(file)

        if p_txt.suffix != '.txt' or p_txt.is_dir():
            continue

        with open(str(p_txt)) as f:
            # アノテーションされているファイルなら
            if f.read()[0] != '0':
                continue

            # image file path
            name = p_txt.name.replace('.txt', '.jpg')

            add_path = f'Images/{dirs[0]}/{name}'
            p_img = target_path.joinpath(add_path)

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
        print(str(path))
        if i == 9:
            print('  ...')
            break
    print()

    # check remove OK?
    is_remove = False
    ans_list = ['y', 'Y', 'yes', 'Yes', 'YES']

    ans = input('Remove OK? (y/N): ')
    if ans in ans_list:
        is_remove = True

    # do not remove
    if not is_remove:
        print('Exit without removing.')
        exit()

    for path in path_list:
        # ファイルが存在するなら
        if path.exists():
            # remove
            path.unlink()
            print(f'deleted: {path}')

    exit()

    """ old script """
    # 引数があれば引数, なければ入力
    # path = argv[1] if len(argv) >= 2 else input('Enter path: ')
    # path = path.replace('\\', '/')

    # if not os.path.exists(path):
    #     print('存在しないディレクトリが入力されました.')
    #     print('パスに￥が含まれる場合はクォーテーションで囲んでください.')
    #     sys.exit(-1)

    # # Labels, Imagesが入っているディレクトリのパス
    # origin_path = ''

    # # 相対パス -> 絶対パスに変換
    # if not pathlib.Path(path).is_absolute():
    #     path = str(pathlib.Path(path).resolve())
    # origin_path = path

    # # 末尾がスラッシュの場合
    # if path.rfind('/') == len(path) - 1:
    #     origin_path = os.path.dirname(path)

    # dir_num = os.path.basename(origin_path)

    # # 001 / 002...などの
    # # 数字n桁のディレクトリで構成されているかどうか (n > 0)
    # if not re.match('[0-9]{1,}', dir_num):
    #     print('ディレクトリの指定場所が異なります.')
    #     print('Labels/***/を指定してください.')
    #     sys.exit(-1)

    # origin_path = os.path.dirname(origin_path)
    # origin_path = os.path.dirname(origin_path)

    # # 削除するファイルのパス
    # path_list = []

    # for (root, _, files) in os.walk(path):
    #     for file in files:
    #         # 一応
    #         if os.path.splitext(file)[1] != '.txt' or os.path.isdir(file):
    #             continue

    #         with open(f'{root}/{file}') as f:
    #             # アノテーションしていないファイルなら
    #             if int(f.read()[0]) == 0:
    #                 bn = os.path.basename(file)
    #                 name = os.path.splitext(bn)[0] + '.jpg'
    #                 p_img = f'{origin_path}/Images/{dir_num}/{name}'

    #                 path_list.append(f'{root}/{file}')  # txt
    #                 path_list.append(p_img)  # jpg

    # for path in path_list:
    #     # ファイルが存在するなら
    #     if os.path.exists(path):
    #         # 削除
    #         os.remove(path)
    #         print(f'deleted: {path}')


if __name__ == '__main__':
    main()
