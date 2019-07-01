# Darknet データセット作成ツール

```
# <MEMO>
convert.py
> 入力ファイルが`inflated_labelsだけを参照するのはどうにかすべき？
> 存在しなかったらLabelsを参照する的な


```



*Description :*

+ `darknet.exe`のファイルがある場所にリポジトリ内のファイルを置く

  もしくは、`darknet.exe`をリポジトリ内に移動（コピー）する



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

<details><summary>クローン時のディレクトリ構造（クリックして展開）</summary><div>



```
# ~\darknet-tools\

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
├─bin
│      ffmpeg.exe
│
└─seqrename-images
        hoge_001.jpg
        hoge_002.jpg
        hoge_003.jpg
```
</div></details>

<br>
<br>

## 実行手順 / 使い方


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

1. `startup-script.bat`にD&D

   ※ BBox-Label-Tool後、`datasets > Images`, `datasets > Labels`にファイルがある状態で行う

<br>

+ `datasets`以下に`inflated_labels`, `obj`フォルダが生成される

+ ```
  # classes.txt の内容
  test
  est
  ```

<br>

<details><summary>ディレクトリ構造（datasets以下）- </summary><div>


```
# ~\darknet-tools\datasets\

C:.
│  classes.txt
│
├─Images
│  ├─001
│  │      test.jpg
│  │      test2.jpg
│  │      test3.jpg
│  │
│  └─002
│          est.jpg
│          est2.jpg
│          est3.jpg
│
├─inflated_labels
│  ├─test
│  │      test2_0.txt
│  │      test2_1.txt
│  │      test2_2.txt
│  │      test2_3.txt
│  │      test2_4.txt
│  │      ...
│  │
│  └─est
│          est2_0.txt
│          est2_1.txt
│          est2_2.txt
│          est2_3.txt
│          est2_4.txt
│          ...
│
├─Labels
│  ├─001
│  │      test.txt
│  │      test2.txt
│  │      test3.txt
│  │
│  └─002
│          est.txt
│          est2.txt
│          est3.txt
│
└─obj
    ├─test
    │      test2_0.jpg
    │      test2_1.jpg
    │      test2_2.jpg
    │      test2_3.jpg
    │      test2_4.jpg
    │      ...
    │
    └─est
            est2_0.jpg
            est2_1.jpg
            est2_2.jpg
            est2_3.jpg
            est2_4.jpg
            ...
```
</div></details>

<br>

***

### ◆ convert.py

1. `startup-script.bat`にD&D

<br>

<br>

## Darknetの実行

+ 学習元データ[darknet53.conv.74](http://pjreddie.com/media/files/darknet53.conv.74) をダウンロードする

  ※ ダウンロード済みの場合はスキップ

  + ダウンロードしたファイルは`darknet.exe`と同じ階層に置く

+ クローンした`alexeyAB/darknet`内の、`darknet` > `cfg` > `yolov3.cfg`ファイルをコピーして`darknet.exe`と同じ階層に置く

+ 

+ # ここclasses=n, filters=3*(n+5)かく

+ 訓練コマンドを実行する

  ```
  .\darknet.exe detector train .\datasets\config\learning.data .\datasets\config\learning.cfg .\darknet53.conv.74
  ```

  



<br>





