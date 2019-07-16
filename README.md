# Darknet データセット作成ツール

*Description :*

+ `darknet.exe`のファイルがある場所にリポジトリ内のファイルを置く
+ もしくは、`darknet.exe`をリポジトリ内に移動（コピー）する

<br>

### Tools

| ツール             | 簡単な説明                     |
| :----------------- | :----------------------------- |
| BBox-Label-Tool.py | ラベル付け                     |
| convert.py         | 座標をyolo形式に変換           |
| inflate_images.py  | 画像増幅                       |
| seqrename.sh       | 画像ファイルの名前を連番にする |
| bin `<dir>`        | 拡張子変換用など               |

<br>

### 実行に必要なもの

※ インストールしている場合はスキップ

+ bash
+ Python
+ Pillow

<br>

1. Git for Windows のインストール

   > + 基本的にはデフォルトのままで進めていけばOK
   >
   > 公式：https://gitforwindows.org/  
   > 参考：[自分用 Git For Windwosのインストール手順 - Qiita](https://qiita.com/toshi-click/items/dcf3dd48fdc74c91b409)
   >
   > <br>
   >
   > + Gitインストール先`{~}/Git/bin`を環境変数のパスに設定する
   >
   > + コマンドプロンプトを開いて`bash --help`を実行できるか確認する
   >
   >   ※ このとき`'bash'は、内部コマンドまたは外部コマンド ...`と出力された場合は、コマンドプロンプトを再起動、パスの確認などをする



Python のインストール

1. > 公式：<a href="https://www.python.org/" target="_blank">https://www.python.org/</a>  
   > 参考：<a href="https://www.python.jp/install/windows/install_py3.html" target="_blank">Python3のインストール - python.jp</a>
   >   <br>
   >
   > - 環境変数に`{~}/PythonXX/`, `{~}/PythonXX/Scripts/`が設定されているかどうか確認する
   >
   > - コマンドプロンプトを開いて`python --version`, `pip --version`を実行してバージョンが出力されることを確認する
   >
   >   - Python2をインストールしている場合は、`python`→`python3` / `pip`→`pip3`を用いる
   >
   > - Pillowをインストールする
   >
   >   ```
   >   pip install Pillow
   >   ```

<br>

<br>

### ディレクトリ構造

<details><summary>クローン時（クリックして展開）</summary><div>


```
# ~\darknet-tools\

C:.
│  darknet.exe
│  ...
│  BBox-Label-Tool.py
│  convert.py
│  inflate_images.py
│  README.md
│  seqrename.sh
│  
├─bin
│      ffmpeg.exe
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
        hoge_001.jpg
        hoge_002.jpg
        hoge_003.jpg
```
</div></details>

<br>
<br>

## 実行手順 / 使い方

※ コマンドプロンプト / bash で実行する




### ◆ seqrename.sh

※ すでに連番である場合は実行しなくてよい  

1. `seq-images`フォルダに連番にしたい画像を入れる

1. 以下を実行する

     ```
     bash seqrename.sh
     ```

1. `> Enter new file name:`に新しいファイル名を入力する
     ※ data_001.jpg... としたい場合は、`data_`と入力する



+ 実行時に引数を1つ追加すると引数の文字列がファイル名になる

  ```
  bash seqrename.sh newgame
  ```

  > newgame001.jpg
  >
  > newgame002.jpg
  >
  > ...

<br>

<br>

### ◆ BBox-Label-Tool.py

1. `datasets/Images`に連番にした画像を置く

   + seqrename.sh を使った場合は`seqrename-images`から移動する

1. 以下を実行する（引数にはフォルダ名を指定）

   ```
   python BBox-Label-Tool.py datasets
   ```

1. <a href="https://github.com/puzzledqs/BBox-Label-Tool#bbox-label-tool" target="_blank">BBox-Label-Tool</a> のREADME.mdのように進めていく

<br>

<br>

### ◆ inflate_images.py

※ 画像の増幅を行わない場合はスキップ

1. `datasets/classes.txt`にクラスを記述する

   ```
   # classes.txt の内容
   test
   est
   ```

2. 以下を実行する（引数にはフォルダ名を指定）

   ```
   python imflate-images.py datasets
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

<br>

### ◆ convert.py

1. 以下を実行する

   ```
   python convert.py datasets
   ```

   + inflate_images.py を実行した場合は、以下をのフォルダを参照する

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

<br>

## Darknetの実行

1. 学習元データ [darknet53.conv.74](http://pjreddie.com/media/files/darknet53.conv.74) をダウンロードする

   ※ ダウンロード済み、または既に学習を始めている場合はスキップ

   + ダウンロードしたファイルは`darknet.exe`と同じ階層に置く
   + クローンした <a href="https://github.com/AlexeyAB/darknet" target="_blank">alexeyAB/darknet</a> の、`darknet/cfg/yolov3.cfg`ファイルをコピーして`darknet-tools/datasets/config/`に置く（ファイル名は`learning.cfg`）

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

<br>






