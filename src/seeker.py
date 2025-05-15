from user import User

class JobSeeker(User):
    def signup_seeker(self, email, password, name, location, phonenum, dob, age, cv_v, experiencelevel, industry):
        userid = self.signup_user(email, password, name, location, 'jobseeker', phonenum, dob, age)
        self.cursor.execute("""
            INSERT INTO jobseeker (userid, cv_v, experiencelevel, industry)
            VALUES (?, ?, ?, ?)""",
            (userid, cv_v, experiencelevel, industry))
        self.conn.commit()

    def update_seeker(self, userid, user_data=None, seeker_data=None):
        if user_data:
            self.update_user(userid, **user_data)
        if seeker_data:
            updates = ", ".join([f"{k}=?" for k in seeker_data])
            values = list(seeker_data.values()) + [userid]
            self.cursor.execute(f"UPDATE jobseeker SET {updates} WHERE userid=?", values)
            self.conn.commit()

    def delete_seeker(self, userid):
        self.cursor.execute("DELETE FROM jobseeker WHERE userid=?", (userid,))
        self.delete_user(userid)

