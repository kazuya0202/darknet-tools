import urllib
import urllib.request
from pathlib import Path
import sys


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


def main():
    # default: yolov3.cfg
    default_cfg = 'cfg/yolov3.cfg'

    argv = sys.argv
    if len(argv) >= 2:
        default_cfg = argv[1]

    cfg = Path(f'./{default_cfg}').with_suffix('.cfg')
    if cfg.exists():
        print(f'Get `{default_cfg}` from local.')
    else:
        print(f'./{default_cfg} is not exists.')
        print(f'Get `{default_cfg}` from alexeyAB/darknet/cfg/{default_cfg}.')
    print()

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

    target = cfg if cfg.exists() else default_cfg
    contents = get_cfg(target)

    # modify
    print('--- Modified ---')

    # batch / subdivisions
    x_list = [
        ['batch=', 'batch ='],
        ['subdivisions=', 'subdivisions ='],
        ['# batch=', '# batch =', '#batch=', '#batch ='],
        ['# subdivisions=', '# subdivisions =', '#subdivisions=', '#subdivisions =']]
    comment_strs = []
    uncomment_strs = []

    n = -1
    for xl in x_list:
        for _ in range(len(contents) - n - 1):
            n += 1
            if any([contents[n].find(x) > -1 for x in xl]):
                c = contents[n]
                idx = c.find('#')

                if idx > -1:
                    t = (c[idx + 1:].strip() + '\n')
                    uncomment_strs.append([n, t])
                else:
                    t = ('# ' + c)
                    comment_strs.append([n, t])

                break

    # uncomment / comment
    if len(comment_strs) == len(uncomment_strs):
        for xn in comment_strs:
            contents[xn[0]] = xn[1]
            print(f'{xn[0]:>3}: {xn[1]}', end='')

    for xn in uncomment_strs:
        contents[xn[0]] = xn[1]
        print(f'{xn[0]:>3}: {xn[1]}', end='')

    # classes / filters / max_batches / steps
    for n, c in enumerate(contents):
        if c.find('classes') > -1:
            idx = find_filter_index(contents, n)
            if idx > -1:
                contents[n] = f'classes={classes}\n'
                contents[idx] = f'filters={filters}\n'

                print(f'{(idx + 1):>3}: {contents[idx]}', end='')
                print(f'{(n + 1):>3}: {contents[n]}', end='')

        if c.find('max_batches') > -1:
            contents[n] = f'max_batches={max_batches}\n'
            print(f'{(n + 1):>3}: {contents[n]}', end='')

        if c.find('steps=') > -1:
            contents[n] = f'steps={steps}\n'
            print(f'{(n + 1):>3}: {contents[n]}', end='')

    # write
    out_cfg = Path('datasets/config/learning.cfg')
    out_cfg.parent.mkdir(parents=True, exist_ok=True)

    with out_cfg.open('w') as f:
        f.writelines(contents)


if __name__ == '__main__':
    main()
