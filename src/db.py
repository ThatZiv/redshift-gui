import sqlite3

init = '''CREATE TABLE IF NOT EXISTS settings
(key TEXT PRIMARY KEY, value REAL)'''

class DB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(init)
        self.conn.commit()

    def set(self, key, val):
        self.cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", [key, val])
        self.conn.commit()

    def get(self, key):
        val = self.cursor.execute('SELECT value FROM settings WHERE key = ?',
            [key]).fetchone()
        return val[0] if val else None

    def __del__(self):
        self.conn.close()
