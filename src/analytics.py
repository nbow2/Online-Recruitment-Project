import sqlite3

class Analytics:
    def __init__(self, db_path='db.sqlite3'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    # a. Most applied job title
    def most_applied_job_title(self):
        self.cursor.execute("""
            SELECT v.title, COUNT(a.applicationid) AS num_applicants
            FROM vacancy v
            JOIN application a ON v.vacancyid = a.vacancyid
            GROUP BY v.title
            ORDER BY num_applicants DESC
            LIMIT 1;
        """)
        return self.cursor.fetchone()

    # b. Job titles with no applicants last month
    def jobs_with_no_applicants_last_month(self):
        self.cursor.execute("""
            SELECT v.title
            FROM vacancy v
            LEFT JOIN application a
              ON v.vacancyid = a.vacancyid
              AND strftime('%Y-%m', a.dateapplied) = strftime('%Y-%m', 'now', '-1 month')
            WHERE a.applicationid IS NULL;
        """)
        return self.cursor.fetchall()

    # c. Employer with the most vacancy announcements
    def top_employer_by_announcements(self):
        self.cursor.execute("""
            SELECT u.name AS employer_name, COUNT(v.vacancyid) AS total_announcements
            FROM vacancy v
            JOIN employer e ON v.employerid = e.employerid
            JOIN user u ON e.userid = u.userid
            GROUP BY e.employerid
            ORDER BY total_announcements DESC
            LIMIT 1;
        """)
        return self.cursor.fetchone()
