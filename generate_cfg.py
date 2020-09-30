import re
import sys
import urllib
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


def find_filter_index(contents, cls_idx):
    while cls_idx != 0:
        c = contents[cls_idx]
        if c.find('filters') > -1:
            return cls_idx
        cls_idx -= 1
    return -1


def get_cfg(cfg):
    contents = []

    if isinstance(cfg, Path):
        with cfg.open() as f:
            contents = f.readlines()

    elif isinstance(cfg, str):
        url = f'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/{cfg}'
        with urllib.request.urlopen(url) as res:
            contents = res.readlines()
            contents = [c.decode('utf-8') for c in contents]

    return contents


def main(cfg_file: Optional[str] = "yolov4-custom.cfg"):
    # default: yolov3.cfg
    # default_cfg = 'cfg/yolov3.cfg'

    if cfg_file is None:
        cfg_file = "yolov4-custom.cfg"

    cfg_path = Path(f'./cfg/{cfg_file}').with_suffix('.cfg')
    if cfg_path.exists():
        print(f'Get `{cfg_file}` from local.')
    else:
        print(f'./cfg/{cfg_file} is not exists.')
        print(f'Get `{cfg_file}` from alexeyAB/darknet/cfg/{cfg_file}.')
    print()

    target = cfg_path if cfg_path.exists() else cfg_file
    contents = get_cfg(target)

    # --- parameters
    cls_path = Path(f'datasets/classes.txt')
    classes = len(cls_path.read_text().strip().split('\n'))
    filters = (classes + 5) * 3
    max_batches = classes * 2000
    steps = [max_batches * 0.8, max_batches * 0.9]
    steps = ','.join([str(int(x)) for x in steps])

    print('--- Parameters ---')
    print(f'* classes = {classes}')
    print(f'* filters = {filters}')
    print(f'* max_batches = {max_batches}')
    print(f'* steps = {steps}')
    print()
    # --------------

    # modify
    print('--- Modified ---')
    # -----
    # pat = re.compile(r"\[[a-z]+\]")

    # # idxs[0] => [net] / idxs[1] => [???]
    # # idxs = [i for i, line in enumerate(contents) if pat.search(line)]

    # idx = [i for i, line in enumerate(contents) if pat.search(line)][1]
    # idx = contents.index(contents[idx])
    # net_param, params = contents[:idx], contents[idx:]

    # @dataclass
    # class IndexValue:
    #     index: int
    #     value: str

    # # extract `batch`, `subdivision`
    # fd_batch = [IndexValue(i, x) for i, x in enumerate(net_param) if x.find("batch") > -1 and not x.find("max_batches") > -1]
    # fd_subdiv = [IndexValue(i, x) for i, x in enumerate(net_param) if x.find("subdivision") > -1]
    # print(fd_batch)
    # print(fd_subdiv)

    # for x in fd_batch:
    #     if x.value.find("#") > -1:
    #         pass

    # net_param.extend(params)
    # contents = net_param

    # batch / subdivisions
    # x_list = [
    #     ['batch=', 'batch ='],
    #     ['subdivisions=', 'subdivisions ='],
    #     ['# batch=', '# batch =', '#batch=', '#batch ='],
    #     ['# subdivisions=', '# subdivisions =', '#subdivisions=', '#subdivisions =']]
    # comment_strs = []
    # uncomment_strs = []

    # n = -1
    # for xl in x_list:
    #     for _ in range(len(contents) - n - 1):
    #         n += 1
    #         if any([contents[n].find(idx) > -1 for idx in xl]):
    #             c = contents[n]
    #             idx = c.find('#')

    #             if idx > -1:
    #                 t = (c[idx + 1:].strip() + '\n')
    #                 uncomment_strs.append([n, t])
    #             else:
    #                 t = ('# ' + c)
    #                 comment_strs.append([n, t])

    #             break

    # # uncomment / comment
    # if len(comment_strs) == len(uncomment_strs):
    #     for xn in comment_strs:
    #         contents[xn[0]] = xn[1]
    #         print(f'{xn[0]:>3}: {xn[1]}', end='')

    # for xn in uncomment_strs:
    #     contents[xn[0]] = xn[1]
    #     print(f'{xn[0]:>3}: {xn[1]}', end='')

    align_num = 5
    # classes / filters / max_batches / steps
    for n, c in enumerate(contents):
        if c.find('classes') > -1:
            idx = find_filter_index(contents, n)
            if idx > -1:
                contents[n] = f'classes={classes}\n'
                contents[idx] = f'filters={filters}\n'

                print(f'{(idx + 1)}:'.rjust(align_num), f'{contents[idx]}', end='')
                print(f'{(n + 1)}:'.rjust(align_num), f'{contents[n]}', end='')

        if c.find('max_batches') > -1:
            contents[n] = f'max_batches={max_batches}\n'
            print(f'{(n + 1)}:'.rjust(align_num), f'{contents[n]}', end='')

        if c.find('steps=') > -1:
            contents[n] = f'steps={steps}\n'
            print(f'{(n + 1)}:'.rjust(align_num), f'{contents[n]}', end='')

    # write
    out_cfg = Path('datasets/config/learning.cfg')
    out_cfg.parent.mkdir(parents=True, exist_ok=True)

    with out_cfg.open('w') as f:
        f.writelines(contents)


if __name__ == '__main__':
    cfg_file = None
    argv = sys.argv
    if len(argv) >= 2:
        cfg_file = argv[1]

    main(cfg_file)
