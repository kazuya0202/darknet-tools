# Darknet データセット作成ツール

### Tools
| ツール             | 簡単な説明                 |
| :----              | :----                |
| BBox-Label-Tool.py | ラベル付け       |
| convert.py         | 座標をyolo形式に変換 |
| inflate_images.py  | 画像増幅             |
|seqrename.sh|画像ファイルの名前を連番にする|
|startup-script.bat | .py \| .shファイルをD&Dすると自動的にスクリプトを実行 |
| ffmpeg `<dir>` | 拡張子変換用 |

> D&D : ドラッグ＆ドロップ

<br>
<br>

<details><summary>クローン時のディレクトリ構造（クリックで展開）</summary><div>


```
# 例
C:.
│  darknet.exe
│  ...
│  base.cfg
│  BBox-Label-Tool.py
│  convert.py
│  ffmpeg.exe
│  inflate_images.py
│  README.md
│  seqrename.sh
│  startup-script.bat
│  
├─datasets
│  │  classes.txt
│  │  
│  ├─Images
│  │  ├─001
│  │  │      test.jpg
│  │  │      test2.jpg
│  │  │      test3.jpg
│  │  │
│  │  └─002
│  │          est.jpg
│  │          est2.jpg
│  │          est3.jpg
│  │
│  └─Labels
│      ├─001
│      │      test.txt
│      │      test2.txt
│      │      test3.txt
│      │
│      └─002
│              est.txt
│              est2.txt
│              est3.txt
│
├─ffmpeg
│      ffmpeg.exe
│      ffmpeg.ps1
│      ffmpeg.shim
│
└─seqrename-images
        tsukareta001.jpg
        tsukareta002.jpg
        tsukareta003.jpg
```
</div></details>

<br>
<br>

## 使い方（使う順番に）


### ◆ seqrename.sh

※ すでに連番である場合は実行しなくてよい  

1. `seq-images`フォルダに連番にしたい画像を入れる
1. `startup-script.bat`にD&D
1. `> Enter new file name:`にファイル名を入力する

<br>

***

### ◆ BBox-Label-Tool.py

1. `datasets` > `Images`に連番にした画像を置く
1. `startup-script.bat`にD&D
1. <a href="https://github.com/puzzledqs/BBox-Label-Tool#bbox-label-tool" target="_blank">BBox-Label-Tool</a>のREADME.mdのように進めていく

<br>

***

### ◆ inflate-images.py

1. a

<br>

***

### ◆ convert.py

1. `startup-script.bat`にD&D

<br>

***







