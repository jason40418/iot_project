#!/bin/bash
# Program:
#   用於自動排程執行目前環境參數
# chmod +x /home/user/Location/Of/Script
# History:
# 2019/12/11	Ver.1.0.0 Release

cd /home/pi/iot_project
echo -e "====== 開始執行環境偵測 ====== \a \n"
python3 AutoMonitor.py
echo -e "====== 環境偵測完成，已更新至資料庫 ====== \a \n"
