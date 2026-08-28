#!/bin/bash
cd $HOME/your_empire_folder_path  # 請將此處改為您存放帝國專案的實際資料夾路徑
nohup ./start_empire.sh > empire_background.log 2>&1 &

