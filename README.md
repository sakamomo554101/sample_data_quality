# sample_data_quality

下記のライブラリを使って、データ品質やバイアス・ドリフト検知を行うサンプルコードをまとめたリポジトリとなります.

* [deequ](https://github.com/awslabs/python-deequ)


# requirements

* docker
* docker-compose

# setup the environment of deequ

## build docker image

```
cd deequ
docker build -t sample_deequ:1.0 .
```

## run docker container

```
docker run -it -v /<リポジトリをダウンロードしたフォルダの絶対パス>/sample_data_quality/deequ/:/home/codes sample_deequ:1.0 /bin/bash
```

## execute sample code

dockerコンテナ上で実行する

```
python sample_deequ.py
```

# setup the environment of jupyter notebook

## create notebook instance with docker

リポジトリのrootフォルダーで下記を実行する.

```
docker-compose up -d
```

docker imageをリビルドする場合は下記.

```
docker-compose up --build -d
```

## use the notebook

下記をホストマシンのブラウザに入力する.

* http://localhost:8888

jupyter notebook環境で作成したnotebookファイルや他ファイルについては, notebookフォルダに格納される.

<br>
notebook上で下記のコードを追加し, JAVA SDKのパスを設定する.

```
%env JAVA_HOME=/root/.sdkman/candidates/java/current
```