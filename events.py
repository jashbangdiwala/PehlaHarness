import sqlite3, json, time

db = sqlite3.connect("ea.db")
db.execute("""CREATE TABLE IF NOT EXISTS events(
  id INTEGER PRIMARY KEY, ts REAL, kind TEXT,
  domain TEXT, payload TEXT, parent_id INTEGER)""")

def log(kind, payload, domain="core", parent_id=None):
    cur = db.execute(
        "INSERT INTO events(ts,kind,domain,payload,parent_id) VALUES(?,?,?,?,?)",
        (time.time(), kind, domain, json.dumps(payload), parent_id))
    db.commit()
    return cur.lastrowid