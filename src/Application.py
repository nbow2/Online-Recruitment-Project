import sqlite3

class Application:
    def __init__(self, db_path='db.sqlite3'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_application(self, seekerid, vacancyid, dateapplied=None, industry=None):
        self.cursor.execute("""
            INSERT INTO application (seekerid, vacancyid, dateapplied, industry)
            VALUES (?, ?, COALESCE(?, DATE('now')), ?)""",
            (seekerid, vacancyid, dateapplied, industry))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_application(self, applicationid, **application_data):
        if application_data:
            updates = ", ".join([f"{k}=?" for k in application_data])
            values = list(application_data.values()) + [applicationid]
            self.cursor.execute(f"UPDATE application SET {updates} WHERE applicationid=?", values)
            self.conn.commit()

    def delete_application(self, applicationid):
        self.cursor.execute("DELETE FROM application WHERE applicationid=?", (applicationid,))
        self.conn.commit()
