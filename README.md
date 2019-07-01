# Darknet データセット作成ツール

### Tools
| ツール             | 簡単な説明                 |
| :---:              | :---:                |
| BBox-Label-Tool.py | ラベル付け         |
| convert.py         | 座標をyolo形式に変換 |
| inflate_images.py  | 画像増幅             |
|seqrename.sh|画像ファイルの名前を連番にする|
|startup-script.bat | 上のファイルをD&Dするとスクリプトを実行する|

<br>
<br>

<details><summary>ディレクトリ構造（クリックで展開）</summary><div>

```
# 例
C:.
│  darknet.exe
│  ...
│  base.cfg
│  BBox-Label-Tool.py
│  convert.py
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
1. `> Enter name:`にファイル名を入力する

***

### ◆ BBox-Label-Tool.py

1. `startup-script.bat`にD&D
1. <a href="https://github.com/puzzledqs/BBox-Label-Tool" target="_blank">BBox-Label-Tool</a>のREADME.mdのように進めていく

***

### ◆ convert.py

1. 

***







