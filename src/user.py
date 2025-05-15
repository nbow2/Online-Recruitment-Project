import sqlite3

class User:
    def __init__(self, db_path='db.sqlite3'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def signup_user(self, email, password, name, location, usertype, phonenum, dob, age):
        self.cursor.execute("""
            INSERT INTO [user] (email, password, name, location, usertype, phonenum, dob, age)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (email, password, name, location, usertype, phonenum, dob, age))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_user(self, userid, **kwargs):
        if not kwargs:
            return
        updates = ", ".join([f"{k}=?" for k in kwargs])
        values = list(kwargs.values()) + [userid]
        self.cursor.execute(f"UPDATE [user] SET {updates} WHERE userid=?", values)
        self.conn.commit()

    def delete_user(self, userid):
        self.cursor.execute("DELETE FROM [user] WHERE userid=?", (userid,))
        self.conn.commit()

