import random
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Union
from PIL import Image
from sklearn.model_selection import train_test_split

# my packages
import utils.utils as ul

classes = []
all_list = []
is_show = False


def create_config(data_dir: Union[str, Path], train_ratio: Union[int, float]):
    cfg_path = Path(data_dir, 'config')

    if train_ratio > 0:
        train_list, valid_list = train_test_split(
            all_list, test_size=train_ratio, shuffle=True)

        # random.shuffle(all_list)
        # train_num = int(train_ratio * len(all_list))
        # train_list = all_list[:train_num]
        # valid_list = all_list[train_num:]
    else:
        train_list = all_list
        valid_list = all_list

    # train
    path = cfg_path.joinpath('train.txt')
    with open(path, 'w') as train_list_file:
        for file_name in train_list:
            train_list_file.write(file_name + '\n')

    # valid
    path = cfg_path.joinpath('valid.txt')
    with open(path, 'w') as valid_list_file:
        for file_name in valid_list:
            valid_list_file.write(file_name + '\n')

    # data
    path = cfg_path.joinpath('learning.data')
    with open(path, 'w') as data_config:
        size = len(classes)
        cp = cfg_path.as_posix()

        data_config.write(f'classes = {size}\n')
        data_config.write(f'train = {cp}/train.txt\n')
        data_config.write(f'valid = {cp}/valid.txt\n')
        data_config.write(f'names = {cp}/learning.names\n')
        data_config.write('backup = backup\n')

        backup_path = cfg_path.joinpath('backup')
        backup_path.mkdir(parents=True, exist_ok=True)

    # names (classes)
    path = cfg_path.joinpath('learning.names')
    with open(path, 'w') as names_config:
        for cls in classes:
            names_config.write(f'{cls}\n')

    # base_config = open('base.cfg', 'r')
    # new_config = open('{0}/darknet_data/config/learning.cfg'.format(data_dir), 'w')
    # new_config = open('{0}/config/learning.cfg'.format(data_dir), 'w')

    # for line in base_config.readlines():
    #     if line.find('$FILTERS_NUM') != -1:
    #         filter_num = 5 * (len(classes) + 4 + 1)
    #         new_config.write('filters={0}\n'.format(filter_num))
    #     elif line.find('classes') != -1:
    #         new_config.write('classes={0}\n'.format(len(classes)))
    #     else:
    #         new_config.write(line)
    # base_config.close()
    # new_config.close()


def convert(size, box):
    # 変換処理
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[2]) / 2.0
    y = (box[1] + box[3]) / 2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def main(data_dir, obj_dir):
    is_inflated = True  # inflated-imagesを実行したかどうか
    image_dir = obj_dir
    label_dir = 'inflated_labels'

    data_path = Path(data_dir)

    # for is_show == false
    counter = 1

    path = Path(data_dir, label_dir)
    if not path.exists():
        is_inflated = False
        label_dir = 'Labels'
        image_dir = 'Images'
        path = Path(data_dir, label_dir)

    dirs = [x.name for x in path.glob('*') if x.is_dir()]

    # 分類クラス分繰り返す
    for cls, _dir in zip(classes, dirs):
        target_dir = cls if is_inflated else _dir

        # {cls}フォルダが存在しないなら作成
        cls_path = data_path.joinpath(obj_dir, cls)
        cls_path.mkdir(parents=True, exist_ok=True)

        cls_id = classes.index(cls)

        # configフォルダを作成
        cfg_path = data_path.joinpath('config')
        cfg_path.mkdir(parents=True, exist_ok=True)

        label_path = data_path.joinpath(label_dir, target_dir)

        # input ファイル名を取得
        txt_name_list = []
        for fp in label_path.glob('*'):
            txt_name_list.append(fp.name)

        if is_show:
            print(f'txt_name_list = {txt_name_list}')

        img_base_path = Path(data_dir, image_dir, target_dir)

        # input ファイル数分変換処理
        for txt_name in txt_name_list:
            # inputファイルを読み込み、行に分割
            lines = None
            txt_file = label_path.joinpath(txt_name)
            with open(txt_file) as f:
                lines = f.read().replace('\r\n', '\n').split('\n')

            # outputファイル作成
            fname = Path(txt_file).stem + '.jpg'
            txt_save_path = cls_path.joinpath(txt_name)
            img_save_path = cls_path.joinpath(fname)

            img_path = img_base_path.joinpath(fname)
            img = Image.open(img_path)
            w = int(img.size[0])
            h = int(img.size[1])

            # save to {obj_dir}
            if not img_save_path.exists():
                img.save(str(img_save_path))

            is_convert = False
            content = []
            for line in lines:
                elems = line.split(' ')
                if len(elems) != 4:
                    continue

                is_convert = True
                if is_show:
                    print(line + '\n')
                    print(elems)

                # xmin = float(elems[0])
                # xmax = float(elems[2])
                # ymin = float(elems[1])
                # ymax = float(elems[3])
                # b = (xmin, xmax, ymin, ymax)

                b = tuple([float(x) for x in elems])
                bb = convert((w, h), b)

                xx = ' '.join([str(a) for a in bb])
                content.append(f'{cls_id} {xx}\n')

            with open(txt_save_path, 'w') as f:
                f.writelines(content)

            if is_convert:
                all_list.append(img_save_path.as_posix())

            if not is_show:
                all_size = len(txt_name_list)
                print(f'\r * %-10s: {counter} / {all_size}' % cls, end='')
                counter += 1

        if not is_show:
            print()
            counter = 1


if __name__ == '__main__':
    argv = sys.argv

    if ul.has_elems_in_list(argv, '-show'):
        is_show = True

    if len(argv) < 2 and argv[1] != '-show':
        print('please set data directory path.')
        print('python [input_folder] [inflated_images_folder] [learing_ratio] [-show]\n\n')
        exit(-1)
    data_dir = argv[1]

    obj_dir = 'obj'
    if len(argv) >= 3 and argv[2] != '-show':
        obj_dir = argv[2]

    # クラス名のファイルの読み込み
    classes = [line.strip() for line in open(f'{data_dir}/classes.txt', 'r')]
    print('class name = ', end='')
    for cls in classes:
        print(cls, end=' ')
    print()

    # 学習の割合
    train_ratio = -1
    if len(argv) >= 4 and argv[3] != '-show':
        train_ratio = float(argv[3])

    if '-show' in argv:
        is_show = True
        print()

    # メインプログラム
    main(data_dir, obj_dir)
    create_config(data_dir, train_ratio)

    print('\nFinished.')
