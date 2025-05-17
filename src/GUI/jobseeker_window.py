import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox
import sqlite3
from seeker import JobSeeker
from datetime import datetime

#we are missing some application details~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``


class JobSeekerWindow:
    def __init__(self, userid):
        self.userid = userid
        self.root = tk.Tk()
        self.root.title("Job Seeker")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Fetch the user's name from the database
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM user WHERE userid=?", (userid,))
        result = cursor.fetchone()
        conn.close()

        name = result[0] if result else "Unknown"

        tk.Label(self.root, text="Job Seeker Dashboard", font=("Comic Sans MS", 28, "bold"),
                 fg="white", bg="black").pack(pady=30)

        info_frame = tk.Frame(self.root, bg="black")
        info_frame.pack(pady=10)

        tk.Label(info_frame, text=f"Welcome, {name}!", font=("Arial", 16, "bold"),
                 fg="white", bg="black").pack(pady=10)
        tk.Label(info_frame, text=f"User ID: {userid}", font=("Arial", 12),
                 fg="white", bg="black").pack(pady=5)

        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(pady=30)

        # Button 1: Insert Info
        tk.Button(
            btn_frame,
            text="Insert Info",
            bg="blue",
            fg="white",
            font=("Arial", 14, "bold"),
            width=15,
            height=2,
            command=self.open_insert_info_window
        ).grid(row=0, column=0, padx=8, pady=8)

        # Button 2: Update Info
        tk.Button(
            btn_frame,
            text="Update Info",
            bg="blue",
            fg="white",
            font=("Arial", 14, "bold"),
            width=15,
            height=2,
            command=self.open_update_info_window
        ).grid(row=0, column=1, padx=8, pady=8)

        # Button 3: Edit Email/Password
        tk.Button(
            btn_frame,
            text="Edit Email/Password",
            bg="blue",
            fg="white",
            font=("Arial", 14, "bold"),
            width=15,
            height=2,
            command=self.open_edit_email_password_window
        ).grid(row=0, column=2, padx=8, pady=8)

        # Button 4: Vacancy
        tk.Button(
            btn_frame,
            text="Vacancy",
            bg="blue",
            fg="white",
            font=("Arial", 14, "bold"),
            width=15,
            height=2,
            command=self.open_vacancy_window
        ).grid(row=1, column=0, padx=8, pady=8)

        # Button 5: Placeholder
        tk.Button(
            btn_frame,
            text="Saved Jobs",
            bg="blue",
            fg="white",
            font=("Arial", 14, "bold"),
            width=15,
            height=2,
            command=self.open_saved_jobs_window
        ).grid(row=1, column=1, padx=8, pady=8)

        # Button 6: Placeholder
        tk.Button(
            btn_frame,
            text="Applied Jobs",
            bg="blue",
            fg="white",
            font=("Arial", 14, "bold"),
            width=15,
            height=2,
            command=self.open_applied_jobs_window
        ).grid(row=1, column=2, padx=8, pady=8)

        # Button 7: Logout
        tk.Button(
            btn_frame,
            text="Logout",
            bg="blue",
            fg="white",
            font=("Arial", 14, "bold"),
            width=15,
            height=2,
            command=self.logout
        ).grid(row=2, column=1, padx=8, pady=8)

        self.root.mainloop()

    def open_insert_info_window(self):
        insert_win = tk.Toplevel(self.root)
        insert_win.title("Insert Seeker Info")
        insert_win.geometry("500x350")
        insert_win.configure(bg="black")

        tk.Label(insert_win, text="Insert Your Info", font=("Arial", 16, "bold"),
                 fg="white", bg="black").pack(pady=10)

        form_frame = tk.Frame(insert_win, bg="black")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="CV (PDF):", bg="black", fg="white",
                 font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        cv_path_var = tk.StringVar()
        cv_entry = tk.Entry(form_frame, font=("Arial", 12),
                            width=25, textvariable=cv_path_var, state="readonly")
        cv_entry.grid(row=0, column=1, pady=5)

        def browse_cv():
            file_path = fd.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file_path:
                cv_path_var.set(file_path)

        tk.Button(form_frame, text="Browse", command=browse_cv, bg="blue",
                  fg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5)

        tk.Label(form_frame, text="Experience Level:", bg="black", fg="white", font=(
            "Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        exp_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        exp_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Industry:", bg="black", fg="white",
                 font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
        industry_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        industry_entry.grid(row=2, column=1, pady=5)

        def save_info():
            cv_v = cv_path_var.get()
            experiencelevel = exp_entry.get()
            industry = industry_entry.get()
            seeker = JobSeeker()
            seeker.insert_seeker_info(
                self.userid, cv_v, experiencelevel, industry)
            messagebox.showinfo("Success", "Info inserted successfully!")
            insert_win.destroy()

        tk.Button(insert_win, text="Save", command=save_info, bg="blue", fg="white",
                  font=("Arial", 12, "bold"), width=10).pack(pady=15)

    def open_update_info_window(self):
        update_win = tk.Toplevel(self.root)
        update_win.title("Update Seeker Info")
        update_win.geometry("400x300")
        update_win.configure(bg="black")

        tk.Label(update_win, text="Update Your Info", font=("Arial", 16, "bold"),
                 fg="white", bg="black").pack(pady=10)

        form_frame = tk.Frame(update_win, bg="black")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="CV (PDF):", bg="black", fg="white",
                 font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        cv_path_var = tk.StringVar()
        cv_entry = tk.Entry(form_frame, font=("Arial", 12),
                            width=25, textvariable=cv_path_var, state="readonly")
        cv_entry.grid(row=0, column=1, pady=5)

        def browse_cv():
            file_path = fd.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file_path:
                cv_path_var.set(file_path)

        tk.Button(form_frame, text="Browse", command=browse_cv, bg="blue",
                  fg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5)

        tk.Label(form_frame, text="Experience Level:", bg="black", fg="white", font=(
            "Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        exp_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        exp_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Industry:", bg="black", fg="white",
                 font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
        industry_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        industry_entry.grid(row=2, column=1, pady=5)

        def save_update():
            cv_v = cv_path_var.get()
            experiencelevel = exp_entry.get()
            industry = industry_entry.get()
            seeker = JobSeeker()
            seeker.insert_seeker_info(
                self.userid, cv_v, experiencelevel, industry)
            messagebox.showinfo("Success", "Info updated successfully!")
            update_win.destroy()

        tk.Button(update_win, text="Save", command=save_update, bg="blue", fg="white",
                  font=("Arial", 12, "bold"), width=10).pack(pady=15)

    def open_edit_email_password_window(self):
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Email/Password")
        edit_win.geometry("400x220")
        edit_win.configure(bg="black")

        tk.Label(edit_win, text="Edit Email/Password", font=("Arial", 16, "bold"),
                 fg="white", bg="black").pack(pady=10)

        form_frame = tk.Frame(edit_win, bg="black")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="New Email:", bg="black", fg="white",
                 font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        email_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        email_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="New Password:", bg="black", fg="white", font=(
            "Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        password_entry = tk.Entry(form_frame, font=(
            "Arial", 12), width=25, show="*")
        password_entry.grid(row=1, column=1, pady=5)

        def save_email_password():
            new_email = email_entry.get()
            new_password = password_entry.get()
            seeker = JobSeeker()
            user_data = {}
            if new_email:
                user_data['email'] = new_email
            if new_password:
                user_data['password'] = new_password
            if user_data:
                seeker.update_seeker(self.userid, user_data=user_data)
                messagebox.showinfo(
                    "Success", "Email/Password updated successfully!")
            else:
                messagebox.showwarning(
                    "No Change", "Please enter new email or password.")
            edit_win.destroy()

        tk.Button(edit_win, text="Save", command=save_email_password, bg="blue", fg="white",
                  font=("Arial", 12, "bold"), width=10).pack(pady=15)

    def open_vacancy_window(self):
        vacancy_win = tk.Toplevel(self.root)
        vacancy_win.title("Available Vacancies")
        vacancy_win.geometry("850x500")
        vacancy_win.configure(bg="black")

        tk.Label(vacancy_win, text="Available Vacancies", font=("Comic Sans MS", 20, "bold"),
             fg="white", bg="black").pack(pady=20)

    # Treeview frame
        table_frame = tk.Frame(vacancy_win, bg="black")
        table_frame.pack(fill="both", expand=True, padx=10)

        columns = ("ID", "Title", "Location", "Industry", "Salary")
        tree = ttk.Treeview(table_frame, columns=columns,
                            show='headings', height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center",
                        width=150 if col != "Title" else 200)
            tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    # Load vacancies
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT vacancyid, title, location, industry, salary
            FROM vacancy
            WHERE ishidden = 0
        """)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
            conn.close()

    # Action buttons
        btn_frame = tk.Frame(vacancy_win, bg="black")
        btn_frame.pack(pady=20)

    def open_vacancy_window(self):
        vacancy_win = tk.Toplevel(self.root)
        vacancy_win.title("Available Vacancies")
        vacancy_win.geometry("850x500")
        vacancy_win.configure(bg="black")

        tk.Label(vacancy_win, text="Available Vacancies", font=("Comic Sans MS", 20, "bold"),
                fg="white", bg="black").pack(pady=20)

        # Treeview frame
        table_frame = tk.Frame(vacancy_win, bg="black")
        table_frame.pack(fill="both", expand=True, padx=10)

        columns = ("ID", "Title", "Location", "Industry", "Salary")
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150 if col != "Title" else 200)
        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Load vacancies
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT vacancyid, title, location, industry, salary
            FROM vacancy
            WHERE ishidden = 0
        """)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

        # Action buttons
        btn_frame = tk.Frame(vacancy_win, bg="black")
        btn_frame.pack(pady=20)

        def apply_to_selected():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("Select Vacancy", "Please select a vacancy to apply.")
                return
            vacancyid = tree.item(selected)["values"][0]

            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM application
                WHERE seekerid=? AND vacancyid=?
            """, (self.userid, vacancyid))
            if cursor.fetchone():
                messagebox.showinfo("Already Applied", "You have already applied to this vacancy.")
            else:
                cursor.execute("""
                    INSERT INTO application (seekerid, vacancyid, dateapplied, industry)
                    VALUES (?, ?, ?, (SELECT industry FROM vacancy WHERE vacancyid=?))
                """, (self.userid, vacancyid, datetime.now().strftime("%Y-%m-%d"), vacancyid))
                conn.commit()
                messagebox.showinfo("Success", "Application submitted!")
            conn.close()

        def save_selected():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("Select Vacancy", "Please select a vacancy to save.")
                return
            vacancyid = tree.item(selected)["values"][0]

            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM savedvacancy
                WHERE seekerid=? AND vacancyid=?
            """, (self.userid, vacancyid))
            if cursor.fetchone():
                messagebox.showinfo("Already Saved", "This vacancy is already in your saved list.")
            else:
                cursor.execute("""
                    INSERT INTO savedvacancy (seekerid, vacancyid, datesaved)
                    VALUES (?, ?, DATE('now'))
                """, (self.userid, vacancyid))
                conn.commit()
                messagebox.showinfo("Saved", "Vacancy added to saved list.")
            conn.close()

        tk.Button(btn_frame, text="Apply", command=apply_to_selected,
                bg="blue", fg="white", font=("Arial", 14, "bold"),
                width=15, height=2).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Save", command=save_selected,
                bg="blue", fg="white", font=("Arial", 14, "bold"),
                width=15, height=2).pack(side="right", padx=20)

    def open_saved_jobs_window(self):
        saved_win = tk.Toplevel(self.root)
        saved_win.title("Saved Jobs")
        saved_win.geometry("850x450")
        saved_win.configure(bg="black")

        tk.Label(saved_win, text="Your Saved Jobs", font=("Comic Sans MS", 20, "bold"),
                fg="white", bg="black").pack(pady=20)

        table_frame = tk.Frame(saved_win, bg="black")
        table_frame.pack(fill="both", expand=True, padx=10)

        columns = ("ID", "Title", "Location", "Industry", "Saved Date")
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=140 if col != "Title" else 200)
        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Load saved vacancies
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.vacancyid, v.title, v.location, v.industry, s.datesaved
            FROM savedvacancy s
            JOIN vacancy v ON s.vacancyid = v.vacancyid
            WHERE s.seekerid = ?
        """, (self.userid,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

        # Unsave button
        def unsave_selected():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("Select Job", "Please select a job to remove.")
                return
            vacancyid = tree.item(selected)["values"][0]

            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM savedvacancy WHERE seekerid=? AND vacancyid=?", (self.userid, vacancyid))
            conn.commit()
            conn.close()

            tree.delete(selected)
            messagebox.showinfo("Removed", "Job removed from saved list.")

        tk.Button(saved_win, text="Unsave", command=unsave_selected,
                bg="blue", fg="white", font=("Arial", 14, "bold"),
                width=15, height=2).pack(pady=20)

    def open_applied_jobs_window(self):
        applied_win = tk.Toplevel(self.root)
        applied_win.title("Applied Jobs")
        applied_win.geometry("900x450")
        applied_win.configure(bg="black")

        tk.Label(applied_win, text="Jobs You've Applied To", font=("Comic Sans MS", 20, "bold"),
                fg="white", bg="black").pack(pady=20)

        from tkinter import ttk
        table_frame = tk.Frame(applied_win, bg="black")
        table_frame.pack(fill="both", expand=True, padx=10)

        columns = ("ID", "Title", "Location", "Industry", "Date Applied", "Review Status")
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=140 if col != "Title" else 200)
        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Load applied jobs
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.vacancyid, v.title, v.location, v.industry, a.dateapplied,
                COALESCE(ad.reviewstatus, 'Pending')
            FROM application a
            JOIN vacancy v ON a.vacancyid = v.vacancyid
            LEFT JOIN applicationdetail ad ON ad.applicationid = a.applicationid
            WHERE a.seekerid = ?
        """, (self.userid,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def logout(self):
        self.root.destroy()
        from GUI.login import LoginWindow
        LoginWindow()
