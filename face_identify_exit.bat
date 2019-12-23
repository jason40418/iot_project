cd C:\Users\user\Miniconda3\condabin

call conda activate

cd /D Z:\iot_project

python recognize_exit.py --detector model/face/face_detection_model --embedding-model model/face/openface_nn4.small2.v1.t7 --recognizer model/face/output/recognizer.pickle --le model/face/output/le.pickle
