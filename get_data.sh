#!/bin/sh
WORKDIR=./data
mkdir -p ${WORKDIR}
#wget -P $WORKDIR https://github.com/alexcg1/ml-datasets/raw/master/nlp/startrek/startrek_tng.csv

kaggle datasets download -d shubchat/1002-short-stories-from-project-guttenberg
unzip 1002-short-stories-from-project-guttenberg.zip
mv *.csv data/
export JINA_DATA_PATH=data/db_books.csv