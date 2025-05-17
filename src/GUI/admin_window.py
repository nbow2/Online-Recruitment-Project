import tkinter as tk
from tkinter import ttk, messagebox
from admin import Admin

class AdminWindow:
    def __init__(self, userid):
        self.userid = userid
        self.admin = Admin()
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

        tab_control.add(self.user_tab, text="Users")
        tab_control.add(self.vacancy_tab, text="Vacancies")

        self.init_user_tab()
        self.init_vacancy_tab()

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
                  bg="red", fg="white", font=("Arial", 12, "bold"), width=15).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Promote to Admin", command=self.promote_user,
                  bg="red", fg="white", font=("Arial", 12, "bold"), width=18).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Demote Admin", command=self.demote_user,
                  bg="red", fg="white", font=("Arial", 12, "bold"), width=18).pack(side="left", padx=10)

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
                  bg="red", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=10)

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
