from Application import Application

class ApplicationDetail(Application):

    def __init__(self, db_path='db.sqlite3'):
        super().__init__(db_path)

    def add_detail(self, applicationid, coverletter=None, interviewnotes=None,
                   reviewstatus='Pending', reviewerid=None, lastupdated=None):
        self.cursor.execute("""
            INSERT INTO applicationdetail (
                applicationid, coverletter, interviewnotes, reviewstatus, reviewerid, lastupdated
            ) VALUES (?, ?, ?, ?, ?, COALESCE(?, DATETIME('now')))""",
            (applicationid, coverletter, interviewnotes, reviewstatus, reviewerid, lastupdated))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_detail(self, detailid, detail_data=None):
        if detail_data:
            updates = ", ".join([f"{k}=?" for k in detail_data])
            values = list(detail_data.values()) + [detailid]
            self.cursor.execute(f"UPDATE applicationdetail SET {updates} WHERE detailid=?", values)
            self.conn.commit()

    def delete_detail_by_application(self, applicationid):
        self.cursor.execute("DELETE FROM applicationdetail WHERE applicationid=?", (applicationid,))
        self.conn.commit()

    def get_detail_by_application(self, applicationid):
        self.cursor.execute("""
            SELECT detailid, coverletter, interviewnotes, reviewstatus, reviewerid, lastupdated
            FROM applicationdetail
            WHERE applicationid=?""",
            (applicationid,))
        return self.cursor.fetchone()

    def get_full_details(self):
        self.cursor.execute("""
            SELECT
                ad.detailid,
                a.applicationid,
                u1.name AS seeker_name,
                v.title AS vacancy_title,
                ad.coverletter,
                ad.interviewnotes,
                ad.reviewstatus,
                u2.name AS reviewer_name,
                ad.lastupdated
            FROM applicationdetail ad
            JOIN application a ON ad.applicationid = a.applicationid
            JOIN jobseeker js ON a.seekerid = js.seekerid
            JOIN user u1 ON js.userid = u1.userid
            JOIN vacancy v ON a.vacancyid = v.vacancyid
            JOIN employer e ON ad.reviewerid = e.employerid
            JOIN user u2 ON e.userid = u2.userid
        """)
        return self.cursor.fetchall()
