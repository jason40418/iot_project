#!/bin/bash
# Program:
#   用於訓練模型
# History:
# 2019/12/21	Ver.1.0.0 Release


while getopts ":d:b:t:m:r:e:i:" opt
do
   case "$opt" in
      d ) dataset="$OPTARG" ;;
      b ) embeddings="$OPTARG" ;;
      t ) detector="$OPTARG" ;;
      m ) embedding_model="$OPTARG" ;;
      r ) recognizer="$OPTARG" ;;
      e ) le="$OPTARG" ;;
      i ) image="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done



cd /home/pi/iot_project
echo -e "====== 開始執行臉部辨識 ====== \a \n"
python3 recognize.py --detector $detector --embedding-model $embedding_model\
  --recognizer $recognizer --le $le --image $image
echo -e "====== 臉部辨識完成 ====== \a \n"
