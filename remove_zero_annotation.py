import os
import sys
import pathlib
import re


def main():
    argv = sys.argv

    # 引数があれば引数, なければ入力
    path = argv[1] if len(argv) >= 2 else input('Enter path: ')
    path = path.replace('\\', '/')

    if not os.path.exists(path):
        print('存在しないディレクトリが入力されました.')
        print('パスに￥が含まれる場合はクォーテーションで囲んでください.')
        sys.exit(-1)

    # Labels, Imagesが入っているディレクトリのパス
    origin_path = ''

    # 相対パス -> 絶対パスに変換
    if not pathlib.Path(path).is_absolute():
        path = str(pathlib.Path(path).resolve())
    origin_path = path

    # 末尾がスラッシュの場合
    if path.rfind('/') == len(path) - 1:
        origin_path = os.path.dirname(path)

    dir_num = os.path.basename(origin_path)

    # 001 / 002...などの
    # 数字n桁のディレクトリで構成されているかどうか (n > 0)
    if not re.match('[0-9]{1,}', dir_num):
        print('ディレクトリの指定場所が異なります.')
        print('Labels/***/を指定してください.')
        sys.exit(-1)

    origin_path = os.path.dirname(origin_path)
    origin_path = os.path.dirname(origin_path)

    # 削除するファイルのパス
    path_list = []

    for (root, _, files) in os.walk(path):
        for file in files:
            # 一応
            if os.path.splitext(file)[1] != '.txt' or os.path.isdir(file):
                continue

            with open(f'{root}/{file}') as f:
                # アノテーションしていないファイルなら
                if int(f.read()[0]) == 0:
                    bn = os.path.basename(file)
                    name = os.path.splitext(bn)[0] + '.jpg'
                    img_path = f'{origin_path}/Images/{dir_num}/{name}'

                    path_list.append(f'{root}/{file}')  # txt
                    path_list.append(img_path)  # jpg

    for path in path_list:
        # ファイルが存在するなら
        if os.path.exists(path):
            # 削除
            os.remove(path)
            print(f'deleted: {path}')


if __name__ == '__main__':
    main()
