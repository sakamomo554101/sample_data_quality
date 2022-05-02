# sample_data_quality

下記のライブラリを使って、データ品質やバイアス・ドリフト検知を行うサンプルコードをまとめたリポジトリとなります.

* [deequ](https://github.com/awslabs/python-deequ)


# requirements

* docker

# setup the environment of deequ

## build docker image

```
cd deequ
docker build -t sample_deequ:1.0 .
```

## run docker container

```
docker run -it -v /<リポジトリをダウンロードしたフォルダの絶対パス>/sample_data_quality/deequ/:/home/sample_deequ sample_deequ:1.0 /bin/bash
```

## execute sample code

dockerコンテナ上で実行する

```
python sample_deequ.py
```
