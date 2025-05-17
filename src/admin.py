from user import User
import sqlite3

class Admin(User):
    def __init__(self, db_path='db.sqlite3'):
        super().__init__(db_path)

    def get_all_users(self):
        self.cursor.execute("SELECT userid, name, email, usertype FROM user")
        return self.cursor.fetchall()

    def delete_user_by_id(self, userid):
        self.cursor.execute("DELETE FROM user WHERE userid=?", (userid,))
        self.conn.commit()

    def get_all_vacancies(self):
        self.cursor.execute("""
            SELECT v.vacancyid, v.title, v.location, v.industry, v.salary, u.name AS employer_name
            FROM vacancy v
            LEFT JOIN employer e ON v.employerid = e.employerid
            LEFT JOIN user u ON e.userid = u.userid
        """)
        return self.cursor.fetchall()


    def delete_vacancy_by_id(self, vacancyid):
        # Delete related applicationdetail → application → vacancy
        self.cursor.execute("SELECT applicationid FROM application WHERE vacancyid=?", (vacancyid,))
        app_ids = [row[0] for row in self.cursor.fetchall()]
        for appid in app_ids:
            self.cursor.execute("DELETE FROM applicationdetail WHERE applicationid=?", (appid,))
        self.cursor.execute("DELETE FROM application WHERE vacancyid=?", (vacancyid,))
        self.cursor.execute("DELETE FROM vacancy WHERE vacancyid=?", (vacancyid,))
        self.conn.commit()

    def promote_to_admin(self, userid):
        self.cursor.execute("UPDATE user SET usertype='admin' WHERE userid=?", (userid,))
        self.conn.commit()

    def demote_admin(self, userid, to_usertype='jobseeker'):
        self.cursor.execute("UPDATE user SET usertype=? WHERE userid=?", (to_usertype, userid))
        self.conn.commit()
