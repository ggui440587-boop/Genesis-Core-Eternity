import os
import sqlite3
import threading
import time
import datetime
import random

def init_all_systems():
    conn = sqlite3.connect('mesh_master_core.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intel_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_channel TEXT,
            raw_payload TEXT,
            processed_content TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monetization_pipeline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            content_slug TEXT,
            revenue_status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_all_systems()

def multi_source_expansion_worker():
    channels = ["GITHUB_REPOSITORIES", "HUGGINGFACE_MODELS", "TECH_FEEDS", "VECTOR_STORE_SYNC"]
    platforms = ["Shopee_Affiliate", "vocus_Salon", "Google_AdSense", "Social_Broadcast"]
    
    while True:
        try:
            conn = sqlite3.connect('mesh_master_core.db')
            cursor = conn.cursor()
            ch = random.choice(channels)
            raw_data = f"INTEL_NODE_{random.randint(10000,99999)}_SYNC_OK"
            summary_data = f"AI_SUMMARY_REWRITE_{random.randint(100,999)}"
            
            cursor.execute(
                "INSERT INTO intel_stream (source_channel, raw_payload, processed_content, status) VALUES (?, ?, ?, ?)",
                (ch, raw_data, summary_data, "PROCESSED")
            )
            
            pf = random.choice(platforms)
            cursor.execute(
                "INSERT INTO monetization_pipeline (platform, content_slug, revenue_status) VALUES (?, ?, ?)",
                (pf, f"POST_{random.randint(1000,9999)}", "ACTIVE_MONETIZATION")
            )
            
            conn.commit()
            conn.close()
        except:
            pass
        time.sleep(3)

threading.Thread(target=multi_source_expansion_worker, daemon=True).start()

if __name__ == '__main__':
    print("Pipeline Master Running...")
    while True:
        time.sleep(60)
