import tkinter as tk
from tkinter import ttk, messagebox
from admin import Admin
import sqlite3

def show_industry_report(parent):
    report_win = tk.Toplevel(parent)
    report_win.title("Industry Report")
    report_win.geometry("600x400")
    report_win.configure(bg="black")

    tk.Label(report_win, text="Industry Report", font=("Arial", 18, "bold"),
             fg="white", bg="black").pack(pady=15)

    columns = ("Industry", "Total Vacancies", "Total Applications")
    tree = ttk.Treeview(report_win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=180)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            v.industry,
            COUNT(DISTINCT v.vacancyid) AS total_vacancies,
            COUNT(a.applicationid) AS total_applications
        FROM vacancy v
        LEFT JOIN application a ON v.vacancyid = a.vacancyid
        GROUP BY v.industry
        ORDER BY total_applications DESC
    """)
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

class AdminWindow:
    def __init__(self, userid):
        self.userid = userid
        self.admin = Admin()
        self.analytics = self.admin.analytics
        self.operations = self.admin.operations

        self.root = tk.Tk()
        self.root.title("Admin Panel")
        self.root.geometry("950x600")
        self.root.configure(bg="black")

        tk.Label(self.root, text="Admin Dashboard", font=("Comic Sans MS", 28, "bold"),
                 fg="white", bg="black").pack(pady=20)

        tab_control = ttk.Notebook(self.root)
        tab_control.pack(expand=1, fill="both")

        self.user_tab = tk.Frame(tab_control, bg="black")
        self.vacancy_tab = tk.Frame(tab_control, bg="black")
        self.dashboard = tk.Frame(tab_control, bg="black")

        tab_control.add(self.user_tab, text="Users")
        tab_control.add(self.vacancy_tab, text="Vacancies")
        tab_control.add(self.dashboard, text="Dashboard")  

        self.init_user_tab()
        self.init_vacancy_tab()
        self.init_dashboard_tab()

        self.root.mainloop()

    # ------------------------ USERS TAB ------------------------

    def init_user_tab(self):
        columns = ("UserID", "Name", "Email", "Type")
        self.user_tree = ttk.Treeview(self.user_tab, columns=columns, show="headings", height=15)
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, anchor="center", width=200)
        self.user_tree.pack(padx=10, pady=10, fill="both")

        self.load_users()

        btn_frame = tk.Frame(self.user_tab, bg="black")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Delete User", command=self.delete_user,
                  bg="green", fg="white", font=("Arial", 12, "bold"), width=15).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Promote to Admin", command=self.promote_user,
                  bg="green", fg="white", font=("Arial", 12, "bold"), width=18).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Demote Admin", command=self.demote_user,
                  bg="green", fg="white", font=("Arial", 12, "bold"), width=18).pack(side="left", padx=10)

    def load_users(self):
        self.user_tree.delete(*self.user_tree.get_children())
        for row in self.admin.get_all_users():
            self.user_tree.insert("", "end", values=row)

    def delete_user(self):
        selected = self.user_tree.focus()
        if not selected:
            messagebox.showwarning("Select User", "Please select a user to delete.")
            return
        userid = self.user_tree.item(selected)["values"][0]
        if messagebox.askyesno("Confirm", f"Delete user ID {userid}?"):
            self.admin.delete_user_by_id(userid)
            self.load_users()
            messagebox.showinfo("Deleted", "User deleted successfully.")

    def promote_user(self):
        selected = self.user_tree.focus()
        if not selected:
            messagebox.showwarning("Select User", "Please select a user.")
            return
        userid = self.user_tree.item(selected)["values"][0]
        self.admin.promote_to_admin(userid)
        self.load_users()
        messagebox.showinfo("Promoted", "User is now an admin.")

    def demote_user(self):
        selected = self.user_tree.focus()
        if not selected:
            messagebox.showwarning("Select User", "Please select a user.")
            return
        userid = self.user_tree.item(selected)["values"][0]
        self.admin.demote_admin(userid)
        self.load_users()
        messagebox.showinfo("Demoted", "Admin converted to jobseeker.")

    # ------------------------ VACANCIES TAB ------------------------

    def init_vacancy_tab(self):
        columns = ("ID", "Title", "Location", "Industry", "Salary", "Posted By")
        self.vac_tree = ttk.Treeview(self.vacancy_tab, columns=columns, show="headings", height=15)
        for col in columns:
            self.vac_tree.heading(col, text=col)
            self.vac_tree.column(col, anchor="center", width=150)
        self.vac_tree.pack(padx=10, pady=10, fill="both")

        self.load_vacancies()

        tk.Button(self.vacancy_tab, text="Delete Vacancy", command=self.delete_vacancy,
                  bg="green", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=10)

    def load_vacancies(self):
        self.vac_tree.delete(*self.vac_tree.get_children())
        for row in self.admin.get_all_vacancies():
            self.vac_tree.insert("", "end", values=row)

    def delete_vacancy(self):
        selected = self.vac_tree.focus()
        if not selected:
            messagebox.showwarning("Select Vacancy", "Please select a vacancy to delete.")
            return
        vacancyid = self.vac_tree.item(selected)["values"][0]
        if messagebox.askyesno("Confirm", f"Delete vacancy ID {vacancyid} and related applications?"):
            self.admin.delete_vacancy_by_id(vacancyid)
            self.load_vacancies()
            messagebox.showinfo("Deleted", "Vacancy deleted successfully.")

    # ------------------------ DASHBOARD TAB ------------------------

    def init_dashboard_tab(self):
        btn_frame = tk.Frame(self.dashboard, bg="black")
        btn_frame.pack(pady=40)

        buttons = [
            ("Most Applied Job", self.show_most_applied_job),
            ("Jobs w/ 0 Applicants\nLast Month", self.show_jobs_with_no_applicants),
            ("Top Employer", self.show_top_employer),
            ("Search Vacancies", self.search_vacancies),
            ("Search Job Seekers", self.search_job_seekers),
            ("Logout", self.logout)
        ]

        for i, (label, cmd) in enumerate(buttons):
            tk.Button(
                btn_frame,
                text=label,
                bg="green",  # Changed to green
                fg="white",
                font=("Arial", 14, "bold"),
                width=18,
                height=2,
                command=cmd
            ).grid(row=i // 3, column=i % 3, padx=15, pady=15)

        tk.Button(
            btn_frame,
            text="Industry Report",
            bg="green",
            fg="white",
            font=("Arial", 14, "bold"),
            width=20,
            height=2,
            command=lambda: show_industry_report(self.root)
        ).grid(row=2, column=0, padx=8, pady=8)

    def show_most_applied_job(self):
        result = self.analytics.most_applied_job_title()
        if result:
            title, count = result
            messagebox.showinfo("Most Applied Job", f"{title} ({count} applicants)")
        else:
            messagebox.showinfo("No Data", "No applications found.")

    def show_jobs_with_no_applicants(self):
        jobs = self.analytics.jobs_with_no_applicants_last_month()
        if jobs:
            titles = "\n".join(job[0] for job in jobs)
            messagebox.showinfo("Jobs with No Applicants", titles)
        else:
            messagebox.showinfo("No Results", "All jobs received applications last month.")

    def show_top_employer(self):
        result = self.analytics.top_employer_by_announcements()
        if result:
            name, count = result
            messagebox.showinfo("Top Employer", f"{name} with {count} job announcements")
        else:
            messagebox.showinfo("No Data", "No employers found.")

    def search_vacancies(self):
        win = tk.Toplevel(self.root)
        win.title("Search Vacancies")
        win.geometry("400x250")
        win.configure(bg="black")

        tk.Label(win, text="Search Vacancies", font=("Arial", 16, "bold"), fg="white", bg="black").pack(pady=10)

        frame = tk.Frame(win, bg="black")
        frame.pack(pady=10)

        fields = ["Industry", "Location", "Required Experience"]
        vars = {}
        for i, label in enumerate(fields):
            tk.Label(frame, text=label + ":", bg="black", fg="white").grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            vars[label] = entry

        def run_search():
            results = self.operations.search_vacancies(
                vars["Industry"].get(),
                vars["Location"].get(),
                vars["Required Experience"].get()
            )
            if results:
                out = "\n".join(f"{r[1]} | {r[2]} | {r[5]} | {r[6]}" for r in results)
                messagebox.showinfo("Matches", out)
            else:
                messagebox.showinfo("No Matches", "No vacancies match the criteria.")

        tk.Button(win, text="Search", command=run_search, bg="green", fg="white").pack(pady=10)

    def search_job_seekers(self):
        win = tk.Toplevel(self.root)
        win.title("Search Job Seekers")
        win.geometry("400x250")
        win.configure(bg="black")

        tk.Label(win, text="Search Job Seekers", font=("Arial", 16, "bold"), fg="white", bg="black").pack(pady=10)

        frame = tk.Frame(win, bg="black")
        frame.pack(pady=10)

        fields = ["Industry", "Location", "Experience Level"]
        vars = {}
        for i, label in enumerate(fields):
            tk.Label(frame, text=label + ":", bg="black", fg="white").grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            vars[label] = entry

        def run_search():
            results = self.operations.search_job_seekers(
                vars["Industry"].get(),
                vars["Location"].get(),
                vars["Experience Level"].get()
            )
            if results:
                out = "\n".join(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}" for r in results)
                messagebox.showinfo("Matches", out)
            else:
                messagebox.showinfo("No Matches", "No job seekers match the criteria.")

        tk.Button(win, text="Search", command=run_search, bg="green", fg="white").pack(pady=10)

    def logout(self):
        self.root.destroy()
        from GUI.login import LoginWindow
        LoginWindow()
