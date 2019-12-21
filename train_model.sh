#!/bin/bash
# Program:
#   用於訓練模型
# History:
# 2019/12/21	Ver.1.0.0 Release


while getopts ":d:b:t:m:r:e:" opt
do
   case "$opt" in
      d ) dataset="$OPTARG" ;;
      b ) embeddings="$OPTARG" ;;
      t ) detector="$OPTARG" ;;
      m ) embedding_model="$OPTARG" ;;
      r ) recognizer="$OPTARG" ;;
      e ) le="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

cd /home/pi/iot_project/model/face
echo -e "====== 開始執行臉部辨識模型訓練 ====== \a \n"
python3 extract_embeddings.py --dataset $dataset --embeddings $embeddings \
	--detector $detector --embedding-model $embedding_model
echo -e "====== 臉部辨識模型訓練完成 ====== \a \n"
python3 train_model.py --embeddings $embeddings \
  --recognizer $recognizer --le $le
