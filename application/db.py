import sqlite3
import pickle

def init_db():
    con = sqlite3.connect("status_log.db")
    cursor = con.cursor()
    cursor.execute("""DROP TABLE IF EXISTS status""")
    cursor.execute(
        """CREATE TABLE status (
            token TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            data BLOB
        )""")
    cursor.close()
    con.close()

def add_pending_token(token):
    con = sqlite3.connect("status_log.db")
    cursor = con.cursor()
    cursor.execute("""INSERT INTO status (token, status) VALUES(?, ?)""", (token, "pending",))
    con.commit()
    cursor.close()
    con.close()

def update_token_to_complete(token, logs):
    con = sqlite3.connect("status_log.db")
    cursor = con.cursor()
    data = pickle.dumps(logs, pickle.HIGHEST_PROTOCOL)
    cursor.execute("""UPDATE status SET status = ?, data = ?  WHERE token = ?""", ("completed", sqlite3.Binary(data), token,))
    con.commit()
    cursor.close()
    con.close()

def get_token(token):
    con = sqlite3.connect("status_log.db")
    cursor = con.cursor()
    cursor.execute("""SELECT status, data FROM status WHERE token = ?""", (token,))
    result=cursor.fetchone()
    cursor.close()
    con.close()

    if result and result[0] == "completed":
        logs = pickle.loads(result[1])
        return result[0], logs
    else:
        return None, None
