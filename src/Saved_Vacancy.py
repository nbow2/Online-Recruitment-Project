import sqlite3

class SavedVacancy:
    def __init__(self, db_path='db.sqlite3'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def save_vacancy(self, seekerid, vacancyid, datesaved=None):
        self.cursor.execute("""
            INSERT INTO savedvacancy (seekerid, vacancyid, datesaved)
            VALUES (?, ?, COALESCE(?, DATE('now')))""",
            (seekerid, vacancyid, datesaved))
        self.conn.commit()

    def unsave_vacancy(self, seekerid, vacancyid):
        self.cursor.execute("""
            DELETE FROM savedvacancy WHERE seekerid=? AND vacancyid=?""",
            (seekerid, vacancyid))
        self.conn.commit()

    def list_saved(self, seekerid):
        self.cursor.execute("""
            SELECT vacancyid, datesaved FROM savedvacancy WHERE seekerid=?""",
            (seekerid,))
        return self.cursor.fetchall()
