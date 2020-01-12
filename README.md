# Darknet データセット作成ツール

## ツール

| ツール                                                       |                                                             |
| :----------------------------------------------------------- | :---------------------------------------------------------- |
| BBox-Label-Tool.py                                           | アノテーション                                              |
| convert.py                                                   | yolo形式に変換                                              |
| convert2jpg.py                                               | 画像の拡張子を`jpg`に変換する                               |
| generate_cfg.py                                              | `cfg`を自動生成する                                         |
| inflate_images.py                                            | 画像増幅                                                    |
| remove_zero_annotation.py                                    | アノテーションしなかったファイル（`txt` / `jpg`）を削除する |
| seqren.exe（[download](https://github.com/kazuya0202/darknet-tools/releases)） | ファイル名を連番にする                                      |

<br>

## 事前準備

### モジュール / パッケージ

```bash
$ pip install -r requirements.txt
```

+ Pillow
+ opencv-python
+ ffmpeg-python

<br>

### ディレクトリの移動

クローン（zipダウンロード）した`darknet-tools`を、`darknet/build/darknet/x64/`に移動する。

```
~/darknet/build/darknet/x64/darknet-tools/
```

<br>

### ディレクトリ構造

<details><summary>クリックして展開</summary><div>



```
C:.
│  .gitignore
│  BBox-Label-Tool.py
│  convert.py
│  convert2jpg.py
│  generate_cfg.py
│  inflate_images.py
│  README.md
│  remove_zero_annotation.py
│  requirements.txt
│
├─cfg
│      yolov3.cfg
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
│     ├─001
│     │      test.txt
│     │      test2.txt
│     │      test3.txt
│     │
│     └─002
│             est.txt
│             est2.txt
│             est3.txt
│
└─utils
        utils.py
```
</div></details>

<br>

## 使い方

### ◆ seqren.exe

ファイル名を連番に変更する。

※ 必要のない場合はスキップ

<br>

<details><summary>説明（クリックして展開）</summary>


※ [release](https://github.com/kazuya0202/darknet-tools/releases) からダウンロードする。

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

  </details>

<br>

### ◆ convert2jpg.py

画像の拡張子を`jpg`に変換する。

※ 必要のない場合はスキップ

<br>

> + 対象画像の拡張子
>
> ```
> png / jpeg / gif / tif / tiff
> PNG / JPEG / GIF / TIF / TIFF / JPG
> ```

<br>

1. 画像ファイルを任意のフォルダにまとめる

2. 以下を実行する

   ```sh
   $ python convert2jpg.py <画像フォルダ>

   # Example
   $ python convert2jpg.py datasets/Images/001/
   ```
   
   削除対象のファイルがある場合、`y / Y / yes / Yes / YES`のどれかを入力して削除する（誤削除防止）

<br>

### ◆ BBox-Label-Tool.py

アノテーションを行う。

※ アノテーションしなかったファイルは、次の`remove_zero_annotation.py`の実行で削除できるため、消さなくてよい。

<br>

1. `datasets/Images`に画像を置く

1. 以下を実行する

   ```bash
   $ python BBox-Label-Tool.py datasets/
   ```

1. <a href="https://github.com/puzzledqs/BBox-Label-Tool#bbox-label-tool" target="_blank">BBox-Label-Tool</a> のREADME.mdのように進めていく

<br>

### ◆ remove_zero_annotation.py

アノテーションしなかったファイルを全て削除する。

<br>

+ `datasets/Labels/0**/` / `datasets/Images/0**/` を指定する（相対パス・絶対パスどちらでも可）

  ```bash
  $ python remove_zero_annotation.py datasets/Labels/0**/
  # or
  $ python remove_zero_annotation.py datasets/Images/0**/
  ```

  削除対象のファイルがある場合、`y / Y / yes / Yes / YES`のどれかを入力して削除する（誤削除防止）

<br>

### ◆ inflate_images.py

画像の増幅を行う。

※ 行わない場合はスキップ

<br>

1. クラスを記述する

   ```
   # darknet-tools/datasets/classes.txt
   
   test
   est
   ```

2. スクリプトを実行する

   ```bash
   $ python imflate-images.py datasets/
   ```

   ※ BBox-Label-Tool後、`datasets/Images`, `datasets/Labels`にファイルがある状態で行う

+ `datasets`以下に`inflated_labels`, `obj`フォルダが生成される

  > `inflated_labels`：増幅後のラベル
  >
  > `obj`：増幅後の画像

<br>

<details><summary>ディレクトリ構造（クリックして展開）</summary><div>

```
# darknet-tools/datasets/

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

アノテーションファイルを、BBox形式からYOLO形式に変換する。

<br>

+ 以下を実行する

   ```sh
   $ python convert.py datasets/
   ```

> + **inflate_images.py** を実行した場合は、以下をのフォルダを参照する
>
> ```
> ./datasets/inflated_labels/		# ラベル
> ./datasets/obj/[クラス名]/		 # 画像
> ```
>
> + 実行しなかった場合は、以下のフォルダを参照する
>
> ```
> ./datasets/Labels/	# ラベル
> ./datasets/Images/	# 画像
> ```

<br>

### ◆ generate_cfg.py

cfgファイルを自動生成し、実行前に必要な編集を（ある程度）自動的に行う。

+ 以下を実行する

  ```sh
  $ python generate_cfg.py [cfg_name]
  ```

> + `[cfg_name]`を指定しない場合、**cfg/yolov3.cfg** をもとに生成する。（生成先 → **datasets/config/learning.cfg**）
> + `[cfg_name]`には、ローカルにあるもの、もしくは、`alexeyAB/darknet/cfg/`にあるものを指定する。
>   + ローカルにないファイル名を指定された場合、オンライン上から探すため、**yolov3-tiny.cfg** などのファイル名のみを指定する。
>
> <br>
>
> + 変更するパラメータ
>
> ```
> classes
> filters
> max_batches
> steps
> ```
>
> **Note:** これを実行した場合、[#Darknetの実行](#Darknetの実行) の`2, 3`を行う必要はない。ただし、`batch, subdivision`の値は、実行環境によって異なるため、変更する必要がある。

<br>

## Darknetの実行

1. 学習元データ **darknet53.conv.74** をダウンロードする

   + [ダウンロード](http://pjreddie.com/media/files/darknet53.conv.74)
   + ファイルは`darknet.exe`と同じ階層に置く
   
   <br>
   
2. `darknet/cfg/yolov3.cfg`ファイルを`darknet-tools/datasets/config/`にコピーする（ファイル名は`learning.cfg`とする）

   <br>

3. 以下のようにファイルを編集する

   >  **※ Note:**
   >
   > （行頭のコメントアウトを除く）
   >
   > ここでは説明のためコメントを書いているが、コメントを書くと誤作動を招く可能性があるので極力書かないように！
   >

   ```sh
   ## クラス数=2 の場合の例
   
   batch=64	# データセットのサイズに応じて変更（※1）
   subdivisions=8	# GPUの性能などによって値が変わる（※2）
   max_batches=4000	# classes*2000
   steps=3200,3600		# max_batches*0.80, max_batches*0.90
   
   # ......
   
   ### =================
   # classes, filters の値を変更する
   # (重要) filtersの変更箇所は、classesの数行上にある行のみ
   
   # 以下3か所ずつ（classesで検索をかけて見つけること）
   # filters: 603行目, 689行目, 776行目
   # classes: 610行目, 696行目, 783行目 (2019/7/02 現在)
   ### =================
   
   # [convolutional]
   filters=21	# 計算式は後述（※3）
   
   # [yolo]
   classes=2
   ```

   **※1**：`batch=XX`はデータセットのサイズに応じて変更する（数値は2^N^ 値`32, 64, 128, 256 ...` が使われることが多い）

   > ```sh
   > # データセットのサイズ
   > 数百件           >> 32, 64 ...
   > 数千件 ～ 数万件 >> 128, 256 ...
   > ```
   >
   

    <br>

    **※2**：学習を開始したときに、GPUの関係でエラー（*CUDA Error: out of memory*）が発生して中断したときは`subdivision`の値を変更する
   
    ```sh
       subdivision=16	# 8 でダメなら
       subdivision=32	# 16 〃
       subdivision=64	# 32 〃
    ```
   
    > `subdivision`の値が小さいほうが、学習にかかる時間は短くなる。
       >
       > `subdivision`の値が`batch`の値より大きくなることはない。
   
    <br>
   
    **※3**：`filters`の数値は以下の式で計算する
   
    ```bash
       (classes + 5) * 3
    
       # 例
       classes=1  >>  filters=18	# (1+5)*3
       classes=2  >>  filters=21	# (2+5)*3
    ```

<br>

4. 訓練コマンドを実行する

   ```
   .\darknet.exe detector train .\darknet-tools\datasets\config\learning.data .\darknet-tools\datasets\config\learning.cfg .\darknet53.conv.74
   ```

   <br>

   + 学習を再開させる場合、`learning_last.weights`ファイルを指定する

   ```
   .\darknet.exe detector train .\darknet-tools\datasets\config\learning.data .\darknet-tools\datasets\config\learning.cfg .\darknet-tools\datasets\config\backup\learning_last.weights
   ```

