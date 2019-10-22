# Darknet データセット作成ツール

*Description :*

+ `darknet.exe`がある場所にリポジトリ内のファイルを置く

<br>

### ツール

| ツール                    |                                            |
| :------------------------ | :----------------------------------------- |
| BBox-Label-Tool.py        | アノテーション                             |
| convert.py                | yolo形式に変換                             |
| inflate_images.py         | 画像増幅                                   |
| remove_zero_annotation.py | アノテーションしなかったファイルを削除する |
| seqren.exe                | 画像ファイルの名前を連番にする             |
| tojpg.sh                  | 画像の拡張子を`jpg`に変換する              |

<br>

### 実行に必要なもの

+ python
+ (ffmpeg)

<br>

+ モジュール / パッケージ

```bash
$ pip install -r requirements.txt
```

<br>

### ディレクトリ構造

<details><summary>クローン時（クリックして展開）</summary><div>


```
# ~\darknet-tools\

C:.
│  BBox-Label-Tool.py
│  convert.py
│  inflate_images.py
│  README.md
│  seqren.exe
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
└─seqren-images
        hoge_001.jpg
        hoge_002.jpg
        hoge_003.jpg
```
</div></details>

<br>

## 使い方


### ◆ seqren.exe

1. 連番にしたいファイルを任意のフォルダにまとめる

1. 以下を実行する

     ```bash
     $ ./seqren.exe -p {ファイルをまとめたフォルダ}
     ```

     1. `Enter the filename: `に変更後のファイル名を入力する
     2. 確認してOKなら`実行しますか? (y/n): `に`y`を入力する

<br>

+ ファイル名や連番の桁数を指定する場合の詳細

  ```bash
  $ ./seqren.exe --help
  ファイル名を連番にリネームします.
  
  Usage:
    seqren [flags]
  
  Flags:
    -a, --all-show      全てのファイルを表示する
    -f, --force         確認せずに実行する
    -h, --help          help for seqren
    -n, --name string   変更するファイル名 (default "DEFAULT_NAME")
    -p, --path string   ターゲットのパス (default "./")
    -s, --seq int       N桁0埋め (default 3)
  ```

<br>

### ◆ tojpg.sh

※ [ffmpeg](https://ffmpeg.org/) が必要

1. 画像ファイルを任意のフォルダにまとめる

2. 以下を実行する

   ```bash
   $ bash tojpg.sh {まとめたフォルダ}
   ```

 対応している拡張子

> png / jpeg / gif / tif / tiff
> PNG / JPEG / GIF / TIF / TIFF / JPG

<br>

### ◆ BBox-Label-Tool.py

1. `datasets/Images`に連番にした画像を置く

1. 以下を実行する

   ```bash
   $ python BBox-Label-Tool.py datasets
   ```

1. <a href="https://github.com/puzzledqs/BBox-Label-Tool#bbox-label-tool" target="_blank">BBox-Label-Tool</a> のREADME.mdのように進めていく

<br>

### ◆ remove_zero_annotation.py

アノテーションしなかったファイルを全削除

+ `datasets/Labels/0**` を指定する（相対パス・絶対パスどちらでも可）

  ```bash
  $ python remove_zero_annotation.py datasets/Labels/0**
  ```

<br>

### ◆ inflate_images.py

※ 画像の増幅を行わない場合はスキップ

1. **datasets/classes.txt** にクラスを記述する

   ```
   # classes.txt の内容
   test
   est
   ```

2. 以下を実行する

   ```bash
   $ python imflate-images.py datasets
   ```
   
   ※ BBox-Label-Tool後、`datasets/Images`, `datasets/Labels`にファイルがある状態で行う

+ `datasets`以下に`inflated_labels`, `obj`フォルダが生成される

<br>

<details><summary>ディレクトリ構造（クリックして展開）</summary><div>

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
│  │      ...
│  │
│  └─est
│          est2_0.txt
│          est2_1.txt
│          est2_2.txt
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
    │      ...
    │
    └─est
            est2_0.jpg
            est2_1.jpg
            est2_2.jpg
            ...
```
</div></details>

<br>

### ◆ convert.py

1. 以下を実行する

   ```bash
   $ python convert.py datasets
   ```

   + **inflate_images.py** を実行した場合は、以下をのフォルダを参照する

     ```
     ./datasets/inflated-labels/		# ラベル
     ./datasets/obj/{クラス名}/		 # 画像
     ```

   + 実行しなかった場合は、以下のフォルダを参照する

     ```
     ./datasets/Labels/	# ラベル
     ./datasets/Images/	# 画像
     ```

<br>

## Darknetの実行

1. 学習元データ [darknet53.conv.74](http://pjreddie.com/media/files/darknet53.conv.74) をダウンロードする

   + ダウンロードしたファイルは`darknet.exe`と同じ階層に置く
+ `darknet/cfg/yolov3.cfg`ファイル`darknet-tools/datasets/config/`にコピーする（ファイル名は`learning.cfg`）
  
   <br>

2. 以下のようにファイルを編集する

   ```bash
   ## クラス数が2の場合の例
   
   batch=64		# ※1
   subdivisions=8	# ※2
   max_batches=4000	# classes*2000
   steps=3200,3600		# max_batches*0.80, max_batches*0.90
   # ......
   
   
   ## 以下3か所ずつ（filtersはたくさんあるため、classesで検索をかけて見つけること）
   
   ## filters: 603行目, 689行目, 776行目
   ## classes: 610行目, 696行目, 783行目 (2019/7/02 現在)
   ## 計算式は後に記述
   
   # [convolutional]
   # classesの上にあるfiltersの数値だけ変更
   filters=21		# ※3
   
   # [yolo]
   classes=2
   ```

   **※1**：`batch=XX`はデータセットのサイズに応じて変更する（XXには2のn乗の値 `32, 64, 128, 256, 512, 1024, 2048` が使われることが多い）

   > ```bash
   > # データセットのサイズ
   > 数百件 >> 32, 64 ...
   > 数千件 >> 128, 256 ...
   > 数万件 >> 1024, 2048 ...
   > ```
   >
   > 学習がうまくいっておらず、ほかに調整するパラメータがなくなったときはこのバッチサイズを大きくしたり小さくしたりするとよい

   <br>

   **※2**：学習を開始したときに、GPUのメモリの関係でエラーが発生して中断したときは`subdivision`の値を変更する

   ```bash
   subdivision=16	# next to 8
   subdivision=32	# next to 16
   subdivision=64	# next to 32
   ```

   <br>

   **※3**：`filters`の数値は以下の式で計算する

   ```bash
   (classes + 5) * 3
   
   # 例
   classes=1  >>  filters=18	# (1+5)*3
   classes=2  >>  filters=21	# (2+5)*3
   ```

   <br>

3. 訓練コマンドを実行する

   ```
   .\darknet.exe detector train .\datasets\config\learning.data .\datasets\config\learning.cfg .\darknet53.conv.74
   ```

   <br>

4. 学習を再開させる場合、weightsファイルを指定する

   ```
   .\darknet.exe detector train .\datasets\config\learning.data .\datasets\config\learning.cfg .\datasets\config\backup\learning_last.weights
   ```








