import sqlite3
import json
import time

class MeshDatabase:
    def __init__(self, db_name="mesh_core.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS genes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gene_code TEXT UNIQUE,
                timestamp REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS consensus_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term INTEGER,
                leader_id TEXT,
                state_snapshot TEXT,
                timestamp REAL
            )
        ''')
        self.conn.commit()

    def save_gene(self, gene_code: str):
        try:
            self.cursor.execute("INSERT OR IGNORE INTO genes (gene_code, timestamp) VALUES (?, ?)", (gene_code, time.time()))
            self.conn.commit()
        except Exception:
            pass

    def log_consensus(self, term: int, leader_id: str, snapshot: dict):
        self.cursor.execute("INSERT INTO consensus_logs (term, leader_id, state_snapshot, timestamp) VALUES (?, ?, ?, ?)",
                            (term, leader_id, json.dumps(snapshot), time.time()))
        self.conn.commit()

class RaftConsensus:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.current_term = 0
        self.voted_for = None
        self.state = "Follower" # Follower, Candidate, Leader
        self.leader_id = None

    def request_vote(self, term: int, candidate_id: str) -> bool:
        # Raft 投票邏輯：若任期更新且本輪尚未投票，則投票給候選人
        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
            self.state = "Follower"

        if term == self.current_term and (self.voted_for is None or self.voted_for == candidate_id):
            self.voted_for = candidate_id
            return True
        return False
