import sqlite3


class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def execute(self, query, *params):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)

            if query.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
            elif query.strip().upper().startswith("INSERT"):
                result = cursor.lastrowid
            else:
                result = cursor.rowcount

            conn.commit()
            return result
        finally:
            conn.close()
