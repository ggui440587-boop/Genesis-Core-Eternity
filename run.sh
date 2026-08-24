#!/data/data/com.termux/files/usr/bin/bash
cd ~/iron_core
python iron_business_empire.py >> cron_log.txt 2>&1
python auto_sync.py >> cron_log.txt 2>&1
