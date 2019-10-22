import sys
import os
import subprocess
import random
# import time
from os import walk, getcwd
from PIL import Image

classes = []
is_show = False


def create_config(data_dir, train_ratio):
    all_list = []
    for cls in classes:
        with open(f'{data_dir}/config/{cls}_list.txt', 'r') as list_file:
            for file_name in list_file.readlines():
                if not (file_name in all_list):
                    all_list.append(file_name)

    if train_ratio > 0:
        random.shuffle(all_list)
        train_num = int(train_ratio * len(all_list))
        train_list = all_list[:train_num]
        valid_list = all_list[train_num:]
    else:
        train_list = all_list
        valid_list = all_list

    with open(f'{data_dir}/config/train.txt', 'w') as train_list_file:
        for file_name in train_list:
            train_list_file.write(file_name)

    with open(f'{data_dir}/config/valid.txt', 'w') as valid_list_file:
        for file_name in valid_list:
            valid_list_file.write(file_name)

    with open(f'{data_dir}/config/learning.data', 'w') as data_config:
        data_config.write(f'classes = {len(classes)}\n')
        data_config.write(f'train = {data_dir}/config/train.txt\n')
        data_config.write(f'valid = {data_dir}/config/valid.txt\n')
        data_config.write(f'names = {data_dir}/config/learning.names\n')
        data_config.write('backup = backup\n')

        backup_path = f'{data_dir}/config/backup'
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

    with open(f'{data_dir}/config/learning.names', 'w') as names_config:
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
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def main(data_dir, obj_dir):
    is_inflated = True  # inflated-imagesを実行したかどうか
    seq = 1  # フォルダ連番用
    image_dir = obj_dir
    label_dir = 'inflated_labels'

    # for is_show == false
    counter = 1
    all_counter = 1

    if not os.path.exists(f'{data_dir}/{label_dir}'):
        is_inflated = False
        label_dir = 'Labels'
        image_dir = 'Images'

    # 分類クラス分繰り返す
    for cls in classes:
        seq_fill = str(seq).zfill(3)
        target_dir = cls if is_inflated else seq_fill

        label_path = f'{data_dir}/{label_dir}/{target_dir}'

        # {cls}フォルダが存在しないなら作成
        cls_dir = f'{data_dir}/{obj_dir}/{cls}'
        if not os.path.exists(cls_dir):
            os.makedirs(cls_dir)

        wd = getcwd()
        cls_id = classes.index(cls)

        # configフォルダを作成
        conf_dir = f'{data_dir}/config'
        if not os.path.exists(conf_dir):
            os.makedirs(conf_dir)

        # outputファイルのpathが列挙されるリストファイル
        list_file = open(f'{wd}/{data_dir}/config/{cls}_list.txt', 'w')

        # input ファイル名を取得
        txt_name_list = []
        for (dirpath, dirnames, filenames) in walk(label_path):
            txt_name_list.extend(filenames)

        if is_show:
            print(f'txt_name_list = {txt_name_list}')

        all_counter = len(txt_name_list)

        # input ファイル数分変換処理
        for txt_name in txt_name_list:

            # inputファイルを読み込み、行に分割
            lines = None
            with open(f'{label_path}/{txt_name}', 'r') as txt_file:
                lines = txt_file.read().replace('\r\n', '\n').split('\n')

            # outputファイル作成
            txt_outfile = open(f'{cls_dir}/{txt_name}', 'w')

            fname = os.path.splitext(txt_name)[0]
            img_path = f'{data_dir}/{image_dir}/{target_dir}/{fname}.jpg'

            im = Image.open(img_path)
            w = int(im.size[0])
            h = int(im.size[1])

            ct = 0
            for line in lines:
                # if len(line) >= 4:
                if len(line) < 4:
                    continue

                ct += 1
                elems = line.split(' ')

                if is_show:
                    print(line + '\n')
                    print(elems)

                xmin = float(elems[0])
                xmax = float(elems[2])
                ymin = float(elems[1])
                ymax = float(elems[3])

                b = (xmin, xmax, ymin, ymax)
                bb = convert((w, h), b)
                txt_outfile.write(f'{cls_id} %s\n' % ' '.join([str(a) for a in bb]))

            txt_outfile.close()

            if not is_show:
                print(f'\r * %-10s: {counter} / {all_counter}' % cls, end='')
                counter += 1

            if(ct != 0):
                # write path
                list_file.write(f'{img_path}\n')

        list_file.close()
        seq += 1  # 連番を増やす

        if not is_show:
            print()
            counter = 1


if __name__ == '__main__':
    argv = sys.argv

    if len(argv) < 2 and argv[1] != '-show':
        print('please set data directory path.')
        print('python [input_folder] [inflated_images_folder] [learing_ratio]\n\n')
        exit(-1)
    data_dir = argv[1]

    obj_dir = 'obj'
    if len(argv) >= 3 and argv[2] != '-show':
        obj_dir = argv[2]

    # クラス名のファイルの読み込み
    classes = [line.rstrip() for line in open(f'{data_dir}/classes.txt', 'r')]
    print('class name = ', end='')
    for i in classes:
        print(i, end=' ')
    print()

    # 学習の割合
    train_ratio = -1
    if len(argv) >= 4:
        train_ratio = float(argv[3])

    if '-show' in argv:
        is_show = True
        print()

    # メインプログラム
    main(data_dir, obj_dir)
    create_config(data_dir, train_ratio)

    print('\nFinished.')

    # 不要なリストを削除する
    for i in classes:
        subprocess.call(f'del {data_dir}\\config\\{i}_list.txt', shell=True)
