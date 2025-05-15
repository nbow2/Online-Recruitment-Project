import sqlite3

class Operations:
    def __init__(self, db_path='db.sqlite3'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    # 1. Show vacancies matching criteria
    def search_vacancies(self, industry=None, location=None, required_experience=None):
        query = "SELECT * FROM vacancy WHERE ishidden = 0"
        params = []

        if industry:
            query += " AND industry = ?"
            params.append(industry)
        if location:
            query += " AND location = ?"
            params.append(location)
        if required_experience:
            query += " AND requiredexperience = ?"
            params.append(required_experience)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    # 2. Show job seekers matching criteria
    def search_job_seekers(self, industry=None, location=None, experience_level=None):
        query = """
            SELECT u.name, u.location, js.experiencelevel, js.industry
            FROM jobseeker js
            JOIN user u ON js.userid = u.userid
            WHERE 1=1
        """
        params = []

        if industry:
            query += " AND js.industry = ?"
            params.append(industry)
        if location:
            query += " AND u.location = ?"
            params.append(location)
        if experience_level:
            query += " AND js.experiencelevel = ?"
            params.append(experience_level)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    # 3. Apply to a vacancy
    def apply_to_vacancy(self, seekerid, vacancyid, industry=None):
        self.cursor.execute("""
            INSERT INTO application (seekerid, vacancyid, dateapplied, industry)
            VALUES (?, ?, DATE('now'), ?)""",
            (seekerid, vacancyid, industry))
        self.conn.commit()

    # 4. Save a vacancy
    def save_vacancy(self, seekerid, vacancyid):
        self.cursor.execute("""
            INSERT INTO savedvacancy (seekerid, vacancyid, datesaved)
            VALUES (?, ?, DATE('now'))""",
            (seekerid, vacancyid))
        self.conn.commit()

    # 5. Hide a vacancy (by employer)
    def hide_vacancy(self, employerid, vacancyid):
        self.cursor.execute("""
            UPDATE vacancy
            SET ishidden = 1
            WHERE vacancyid = ? AND employerid = ?""",
            (vacancyid, employerid))
        self.conn.commit()
