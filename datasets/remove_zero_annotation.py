import os
import sys


def main():
    argv = sys.argv

    # 引数があれば引数, なければ入力
    path = argv[1] if len(argv) >= 2 else input('Enter path: ')

    if not os.path.exists(path):
        print('存在しないディレクトリが入力されました.')
        print('パスに￥が含まれる場合はクォーテーションで囲んでください.')
        sys.exit(-1)

    path = path.replace('\\', '/')

    # Labels, Imagesが入っているディレクトリのパス
    # origin_path = path

    origin_path = os.path.dirname(os.path.abspath(__file__))

    path = f'{origin_path}/{path}'
    print(path)
    if not os.path.exists(path):
        print("is not exists")
        sys.exit()

    # 末尾がスラッシュの場合
    if path.rfind('/') == len(path) - 1:
        origin_path = os.path.dirname(path)

    dir_num = os.path.basename(origin_path)

    origin_path = os.path.dirname(origin_path)
    origin_path = os.path.dirname(origin_path)

    # 削除するファイルのパス
    path_list = []

    for (root, dirs, files) in os.walk(path):
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
