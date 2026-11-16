import sqlite3, json, time

from config import DB_PATH

def create_table(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS events(
      id INTEGER PRIMARY KEY, ts REAL, kind TEXT,
      domain TEXT, payload TEXT, parent_id INTEGER)""")

db = sqlite3.connect(DB_PATH)
create_table(db)

def log(kind, payload, domain="core", parent_id=None):
    cur = db.execute(
        "INSERT INTO events(ts,kind,domain,payload,parent_id) VALUES(?,?,?,?,?)",
        (time.time(), kind, domain, json.dumps(payload), parent_id))
    db.commit()
    return cur.lastrowid

def recent(domain, kinds, limit):
    """The newest `limit` events of these kinds in this domain, oldest first."""
    marks = ",".join("?" * len(kinds))
    rows = db.execute(
        f"SELECT id, ts, kind, domain, payload, parent_id FROM events "
        f"WHERE domain = ? AND kind IN ({marks}) ORDER BY id DESC LIMIT ?",
        (domain, *kinds, limit)).fetchall()
    return [{"id": r[0], "ts": r[1], "kind": r[2], "domain": r[3],
             "payload": json.loads(r[4]), "parent_id": r[5]}
            for r in reversed(rows)]
