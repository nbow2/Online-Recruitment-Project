import sqlite3

class Vacancy:
    def __init__(self, db_path='db.sqlite3'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_vacancy(self, employerid, title, description, location, industry, salary, requiredexperience, ishidden=False, dateposted=None):
        self.cursor.execute("""
            INSERT INTO vacancy (employerid, title, description, location, industry, salary, requiredexperience, ishidden, dateposted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (employerid, title, description, location, industry, salary, requiredexperience, ishidden, dateposted))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_vacancy(self, vacancyid, **kwargs):
        if not kwargs:
            return
        updates = ", ".join([f"{k}=?" for k in kwargs])
        values = list(kwargs.values()) + [vacancyid]
        self.cursor.execute(f"UPDATE vacancy SET {updates} WHERE vacancyid=?", values)
        self.conn.commit()

    def delete_vacancy(self, vacancyid):
        self.cursor.execute("DELETE FROM vacancy WHERE vacancyid=?", (vacancyid,))
        self.conn.commit()
