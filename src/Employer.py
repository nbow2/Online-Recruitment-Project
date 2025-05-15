from user import User

class Employer(User):
    
    def __init__(self, db_path='db.sqlite3'):
        super().__init__(db_path)   
    

    def signup_employer(self, email, password, name, location, phonenum, dob, age, company_name, company_description, industry):
        userid = self.signup_user(email, password, name, location, 'employer', phonenum, dob, age)
        self.cursor.execute("""
            INSERT INTO employer (userid, company_name, company_description, industry)
            VALUES (?, ?, ?, ?)""",
            (userid, company_name, company_description, industry))
        self.conn.commit()

    def update_employer(self, userid, user_data=None, employer_data=None):
        if user_data:
            self.update_user(userid, **user_data)
        if employer_data:
            updates = ", ".join([f"{k}=?" for k in employer_data])
            values = list(employer_data.values()) + [userid]
            self.cursor.execute(f"UPDATE employer SET {updates} WHERE userid=?", values)
            self.conn.commit()

    def delete_employer(self, userid):
        self.cursor.execute("DELETE FROM employer WHERE userid=?", (userid,))
        self.delete_user(userid)

