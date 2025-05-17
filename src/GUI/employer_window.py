import tkinter as tk
import sqlite3
from tkinter import ttk

class EmployerWindow:
    def __init__(self, userid):
        self.userid = userid
        self.root = tk.Tk()
        self.root.title("Employer")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Fetch employer name
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM user WHERE userid=?", (userid,))
        result = cursor.fetchone()
        conn.close()
        name = result[0] if result else "Unknown"

        # Header
        tk.Label(self.root, text="Employer Dashboard", font=("Comic Sans MS", 28, "bold"),
                 fg="white", bg="black").pack(pady=30)

        # Info block
        info_frame = tk.Frame(self.root, bg="black")
        info_frame.pack(pady=10)

        tk.Label(info_frame, text=f"Welcome, {name}!", font=("Arial", 16, "bold"),
                 fg="white", bg="black").pack(pady=10)
        tk.Label(info_frame, text=f"User ID: {self.userid}", font=("Arial", 12),
                 fg="white", bg="black").pack(pady=5)

        # Button panel
        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(pady=30)

        buttons = [
            ("Post Job", self.open_post_job_window),
            ("My Vacancies", self.open_my_vacancies_window),
            ("View Applications", self.open_applications_window),
            ("Edit Company Info", self.open_edit_company_window),
            ("View Profile", self.open_view_company_window),
            ("Review Application Details", self.open_review_details_window)
        ]

        for i, (label, action) in enumerate(buttons, 1):
            row = 0 if i <= 3 else 1
            col = (i - 1) % 3
            tk.Button(
                btn_frame,
                text=label,
                bg="red",
                fg="white",
                font=("Arial", 14, "bold"),
                width=20,
                height=2,
                command=action
            ).grid(row=row, column=col, padx=8, pady=8)

        self.root.mainloop()

    # Placeholder methods to be implemented
    def open_post_job_window(self):
        post_win = tk.Toplevel(self.root)
        post_win.title("Post a New Job")
        post_win.geometry("600x500")
        post_win.configure(bg="black")

        tk.Label(post_win, text="Post a New Job", font=("Comic Sans MS", 20, "bold"),
                fg="white", bg="black").pack(pady=20)

        form_frame = tk.Frame(post_win, bg="black")
        form_frame.pack(pady=10)

        labels = [
            "Job Title", "Description", "Location", "Industry",
            "Salary (e.g. 60000)", "Required Experience"
        ]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", font=("Arial", 12), fg="white", bg="black").grid(row=i, column=0, sticky="e", pady=5, padx=10)
            entry = tk.Entry(form_frame, font=("Arial", 12), width=35)
            entry.grid(row=i, column=1, pady=5)
            entries[label] = entry

        def post_job():
            import datetime
            title = entries["Job Title"].get()
            description = entries["Description"].get()
            location = entries["Location"].get()
            industry = entries["Industry"].get()
            salary = entries["Salary (e.g. 60000)"].get()
            experience = entries["Required Experience"].get()

            if not all([title, description, location, industry, salary, experience]):
                tk.messagebox.showwarning("Missing Info", "Please fill in all fields.")
                return

            try:
                salary_value = float(salary)
            except ValueError:
                tk.messagebox.showerror("Invalid Salary", "Salary must be a number.")
                return

            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()

            cursor.execute("""
                SELECT employerid FROM employer WHERE userid=?
            """, (self.userid,))
            result = cursor.fetchone()
            if not result:
                tk.messagebox.showerror("Error", "Employer profile not found.")
                conn.close()
                return

            employeeid = result[0]

            cursor.execute("""
                INSERT INTO vacancy (employerid, title, description, location, industry, salary, requiredexperience, ishidden, dateposted)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
            """, (employeeid, title, description, location, industry, salary_value, experience, datetime.date.today()))
            conn.commit()
            conn.close()

            tk.messagebox.showinfo("Success", "Job posted successfully!")
            post_win.destroy()

        tk.Button(post_win, text="Post Job", command=post_job,
                bg="red", fg="white", font=("Arial", 14, "bold"), width=20).pack(pady=20)


    def open_my_vacancies_window(self):
        vac_win = tk.Toplevel(self.root)
        vac_win.title("My Vacancies")
        vac_win.geometry("850x600")
        vac_win.configure(bg="black")

        tk.Label(vac_win, text="My Job Posts", font=("Comic Sans MS", 20, "bold"),
                fg="white", bg="black").pack(pady=20)

        table_frame = tk.Frame(vac_win, bg="black")
        table_frame.pack(fill="both", expand=True, padx=10)

        columns = ("ID", "Title", "Location", "Salary", "Date Posted", "Hidden?")
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120 if col != "Title" else 200)
        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Load vacancies posted by this employer
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT employerid FROM employer WHERE userid=?", (self.userid,))
        result = cursor.fetchone()
        if not result:
            tk.messagebox.showerror("Error", "Employer profile not found.")
            conn.close()
            return

        employeeid = result[0]
        cursor.execute("""
            SELECT vacancyid, title, location, salary, dateposted, ishidden
            FROM vacancy
            WHERE employerid = ?
        """, (employeeid,))
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            display_row = list(row)
            display_row[-1] = "Yes" if row[-1] else "No"
            tree.insert("", "end", values=display_row)

        # Button to toggle visibility
        def toggle_visibility():
            selected = tree.focus()
            if not selected:
                tk.messagebox.showwarning("Select a vacancy", "Please select a vacancy to hide/unhide.")
                return

            values = tree.item(selected)["values"]
            vacancyid = values[0]
            current_status = values[-1] == "Yes"

            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE vacancy
                SET ishidden = ?
                WHERE vacancyid = ? AND employerid = ?
            """, (0 if current_status else 1, vacancyid, employeeid))
            conn.commit()
            conn.close()

            tree.item(selected, values=(
                values[0], values[1], values[2], values[3], values[4],
                "No" if current_status else "Yes"
            ))

            tk.messagebox.showinfo("Success", "Vacancy visibility updated.")

        def delete_vacancy():
            selected = tree.focus()
            if not selected:
                tk.messagebox.showwarning("Select a vacancy", "Please select a vacancy to delete.")
                return

            values = tree.item(selected)["values"]
            vacancyid = values[0]

            confirm = tk.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{values[1]}' and all its applications?")
            if not confirm:
                return

            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()

            # First, get application IDs related to this vacancy
            cursor.execute("SELECT applicationid FROM application WHERE vacancyid=?", (vacancyid,))
            application_ids = [row[0] for row in cursor.fetchall()]

            # Delete applicationdetail entries
            for appid in application_ids:
                cursor.execute("DELETE FROM applicationdetail WHERE applicationid=?", (appid,))

            # Delete applications
            cursor.execute("DELETE FROM application WHERE vacancyid=?", (vacancyid,))

            # Delete the vacancy
            cursor.execute("DELETE FROM vacancy WHERE vacancyid=? AND employerid=?", (vacancyid, employeeid))

            conn.commit()
            conn.close()

            tree.delete(selected)
            tk.messagebox.showinfo("Deleted", "Vacancy and all related applications have been deleted.")

        # Add Delete button under Hide/Unhide
        tk.Button(vac_win, text="Delete", command=delete_vacancy,
                bg="red", fg="white", font=("Arial", 14, "bold"), width=20).pack(pady=10)

        tk.Button(vac_win, text="Hide/Unhide", command=toggle_visibility,
                bg="red", fg="white", font=("Arial", 14, "bold"), width=20).pack(pady=20)

    def open_applications_window(self):
        app_win = tk.Toplevel(self.root)
        app_win.title("Applications for My Vacancies")
        app_win.geometry("900x500")
        app_win.configure(bg="black")

        tk.Label(app_win, text="Select a Vacancy", font=("Comic Sans MS", 20, "bold"),
                fg="white", bg="black").pack(pady=20)

        dropdown_frame = tk.Frame(app_win, bg="black")
        dropdown_frame.pack()

        tk.Label(dropdown_frame, text="My Vacancies:", font=("Arial", 12),
                fg="white", bg="black").pack(side="left", padx=10)

        vacancy_var = tk.StringVar()
        vacancy_menu = ttk.Combobox(dropdown_frame, textvariable=vacancy_var, width=40, state="readonly")
        vacancy_menu.pack(side="left", padx=5)

        # Load this employer's vacancies
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT employerid FROM employer WHERE userid=?", (self.userid,))
        emp = cursor.fetchone()
        if not emp:
            tk.messagebox.showerror("Error", "Employer profile not found.")
            return

        employeeid = emp[0]
        cursor.execute("""
            SELECT vacancyid, title FROM vacancy WHERE employerid = ?
        """, (employeeid,))
        vacancies = cursor.fetchall()
        conn.close()

        vacancy_map = {f"{v[1]} (ID: {v[0]})": v[0] for v in vacancies}
        vacancy_menu['values'] = list(vacancy_map.keys())

        # Table setup
        table_frame = tk.Frame(app_win, bg="black")
        table_frame.pack(fill="both", expand=True, padx=10, pady=20)

        columns = ("Name", "Email", "Experience", "Applied Date")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180 if col == "Email" else 150)
        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        def load_applications(event=None):
            tree.delete(*tree.get_children())
            selected_label = vacancy_var.get()
            if not selected_label:
                return
            vacancyid = vacancy_map[selected_label]

            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.name, u.email, js.experiencelevel, a.dateapplied
                FROM application a
                JOIN jobseeker js ON a.seekerid = js.seekerid
                JOIN user u ON js.userid = u.userid
                WHERE a.vacancyid = ?
            """, (vacancyid,))
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                tree.insert("", "end", values=row)

        # Bind dropdown selection
        vacancy_menu.bind("<<ComboboxSelected>>", load_applications)

    def open_edit_company_window(self):
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Company Info")
        edit_win.geometry("500x350")
        edit_win.configure(bg="black")

        tk.Label(edit_win, text="Edit Company Info", font=("Comic Sans MS", 20, "bold"),
                fg="white", bg="black").pack(pady=20)

        form_frame = tk.Frame(edit_win, bg="black")
        form_frame.pack(pady=10)

        # Fetch current info
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT company_name, company_description, industry
            FROM employer
            WHERE userid=?
        """, (self.userid,))
        result = cursor.fetchone()
        conn.close()

        company_name = result[0] if result else ""
        company_desc = result[1] if result else ""
        industry = result[2] if result else ""

        # Labels + fields
        tk.Label(form_frame, text="Company Name:", bg="black", fg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=8)
        name_entry = tk.Entry(form_frame, font=("Arial", 12), width=35)
        name_entry.insert(0, company_name)
        name_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Description:", bg="black", fg="white", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=8)
        desc_entry = tk.Entry(form_frame, font=("Arial", 12), width=35)
        desc_entry.insert(0, company_desc)
        desc_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Industry:", bg="black", fg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=5, pady=8)
        industry_entry = tk.Entry(form_frame, font=("Arial", 12), width=35)
        industry_entry.insert(0, industry)
        industry_entry.grid(row=2, column=1)

        # Save button
        def save_info():
            new_name = name_entry.get()
            new_desc = desc_entry.get()
            new_industry = industry_entry.get()

            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE employer
                SET company_name=?, company_description=?, industry=?
                WHERE userid=?
            """, (new_name, new_desc, new_industry, self.userid))
            conn.commit()
            conn.close()

            tk.messagebox.showinfo("Success", "Company info updated.")
            edit_win.destroy()

        tk.Button(edit_win, text="Save", command=save_info,
                bg="red", fg="white", font=("Arial", 12, "bold"),
                width=20).pack(pady=20)


    def open_view_company_window(self):
        view_win = tk.Toplevel(self.root)
        view_win.title("Company Profile")
        view_win.geometry("500x400")
        view_win.configure(bg="black")

        tk.Label(view_win, text="Company Profile", font=("Comic Sans MS", 20, "bold"),
                fg="white", bg="black").pack(pady=20)

        info_frame = tk.Frame(view_win, bg="black")
        info_frame.pack(pady=10)

        # Get user + employer info
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()

        cursor.execute("SELECT name, email, location, phonenum FROM user WHERE userid=?", (self.userid,))
        user_info = cursor.fetchone()

        cursor.execute("SELECT company_name, company_description, industry FROM employer WHERE userid=?", (self.userid,))
        employer_info = cursor.fetchone()

        conn.close()

        labels = [
            ("Company Name", employer_info[0] if employer_info else ""),
            ("Description", employer_info[1] if employer_info else ""),
            ("Industry", employer_info[2] if employer_info else ""),
            ("Contact Name", user_info[0] if user_info else ""),
            ("Email", user_info[1] if user_info else ""),
            ("Location", user_info[2] if user_info else ""),
            ("Phone", user_info[3] if user_info else "")
        ]

        for i, (label, value) in enumerate(labels):
            tk.Label(info_frame, text=label + ":", bg="black", fg="white", font=("Arial", 12, "bold")).grid(row=i, column=0, sticky="e", padx=10, pady=5)
            tk.Label(info_frame, text=value, bg="black", fg="white", font=("Arial", 12)).grid(row=i, column=1, sticky="w", padx=10, pady=5)


    def open_review_details_window(self):
        review_win = tk.Toplevel(self.root)
        review_win.title("Review Application Details")
        review_win.geometry("1000x550")
        review_win.configure(bg="black")

        tk.Label(review_win, text="Review Applications", font=("Comic Sans MS", 20, "bold"),
                fg="white", bg="black").pack(pady=20)

        dropdown_frame = tk.Frame(review_win, bg="black")
        dropdown_frame.pack()

        tk.Label(dropdown_frame, text="Select Vacancy:", font=("Arial", 12),
                fg="white", bg="black").pack(side="left", padx=10)

        vacancy_var = tk.StringVar()
        vacancy_menu = ttk.Combobox(dropdown_frame, textvariable=vacancy_var, width=50, state="readonly")
        vacancy_menu.pack(side="left", padx=5)

        # Load employer's vacancies
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT employerid FROM employer WHERE userid=?", (self.userid,))
        emp = cursor.fetchone()
        if not emp:
            tk.messagebox.showerror("Error", "Employer profile not found.")
            return
        employeeid = emp[0]
        cursor.execute("SELECT vacancyid, title FROM vacancy WHERE employerid=?", (employeeid,))
        vacancies = cursor.fetchall()
        conn.close()

        vacancy_map = {f"{v[1]} (ID: {v[0]})": v[0] for v in vacancies}
        vacancy_menu["values"] = list(vacancy_map.keys())

        # Treeview
        table_frame = tk.Frame(review_win, bg="black")
        table_frame.pack(fill="both", expand=True, padx=10, pady=15)

        columns = ("AppID", "Name", "Email", "Cover Letter", "Review Status")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150 if col != "Cover Letter" else 250)
        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Form to update status and notes
        form_frame = tk.Frame(review_win, bg="black")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Review Status:", font=("Arial", 12),
                fg="white", bg="black").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        status_var = tk.StringVar()
        status_menu = ttk.Combobox(form_frame, textvariable=status_var, values=[
            "Pending", "Reviewed", "Shortlisted", "Rejected"
        ], state="readonly", width=20)
        status_menu.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Interview Notes:", font=("Arial", 12),
                fg="white", bg="black").grid(row=1, column=0, padx=5, pady=5, sticky="ne")
        notes_entry = tk.Text(form_frame, font=("Arial", 12), width=40, height=4)
        notes_entry.grid(row=1, column=1, pady=5)

        def load_details(event=None):
            tree.delete(*tree.get_children())
            selected = vacancy_var.get()
            if not selected:
                return
            vacancyid = vacancy_map[selected]

            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.applicationid, u.name, u.email,
                    COALESCE(ad.coverletter, 'N/A'),
                    COALESCE(ad.reviewstatus, 'Pending')
                FROM application a
                JOIN jobseeker js ON a.seekerid = js.seekerid
                JOIN user u ON js.userid = u.userid
                LEFT JOIN applicationdetail ad ON a.applicationid = ad.applicationid
                WHERE a.vacancyid = ?
            """, (vacancyid,))
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

        def update_review():
            selected = tree.focus()
            if not selected:
                tk.messagebox.showwarning("Select Application", "Please select an application to update.")
                return

            appid = tree.item(selected)["values"][0]
            status = status_var.get()
            notes = notes_entry.get("1.0", "end").strip()

            if not status:
                tk.messagebox.showwarning("Missing Data", "Please select a status.")
                return

            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            # Insert or update detail
            cursor.execute("""
                SELECT detailid FROM applicationdetail WHERE applicationid=?
            """, (appid,))
            existing = cursor.fetchone()

            if existing:
                cursor.execute("""
                    UPDATE applicationdetail
                    SET reviewstatus=?, interviewnotes=?, reviewerid=?, lastupdated=datetime('now')
                    WHERE applicationid=?
                """, (status, notes, employeeid, appid))
            else:
                cursor.execute("""
                    INSERT INTO applicationdetail (applicationid, coverletter, interviewnotes, reviewstatus, reviewerid)
                    VALUES (?, '', ?, ?, ?)
                """, (appid, notes, status, employeeid))

            conn.commit()
            conn.close()

            tk.messagebox.showinfo("Success", "Application review updated.")
            load_details()

        # Buttons
        tk.Button(review_win, text="Update Review", command=update_review,
                bg="red", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=10)

        # Bind dropdown
        vacancy_menu.bind("<<ComboboxSelected>>", load_details)