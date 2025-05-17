import tkinter as tk
from tkinter import messagebox
import sqlite3
from GUI.jobseeker_window import JobSeekerWindow
from GUI.employer_window import EmployerWindow
from GUI.admin_window import AdminWindow

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("700x500")
        self.root.configure(bg="black")
        tk.Label(self.root, text="Login", font=("Comic Sans MS", 28, "bold"),
                 fg="white", bg="black").pack(pady=30)

        form_frame = tk.Frame(self.root, bg="black")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Email:", bg="black", fg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=10)
        self.email_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.email_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Password:", bg="black", fg="white", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=10)
        self.pass_entry = tk.Entry(form_frame, show="*", font=("Arial", 12), width=30)
        self.pass_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="User Type:", bg="black", fg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=10)
        self.usertype_var = tk.StringVar(value="jobseeker")
        self.usertype_menu = tk.OptionMenu(form_frame, self.usertype_var, "jobseeker", "employer", "admin")
        self.usertype_menu.config(font=("Arial", 12), bg="white")
        self.usertype_menu.grid(row=2, column=1)

        # Show password checkbox
        self.show_pass = tk.BooleanVar()
        tk.Checkbutton(form_frame, text="Show", variable=self.show_pass,
                       command=self.toggle_password_visibility,
                       bg="black", fg="white").grid(row=1, column=2, padx=5)

        tk.Label(form_frame, text="User Type:", bg="black", fg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=10)
        self.usertype_var = tk.StringVar(value="jobseeker")
        self.usertype_menu = tk.OptionMenu(form_frame, self.usertype_var, "jobseeker", "employer", "admin")
        self.usertype_menu.config(font=("Arial", 12), bg="white")
        self.usertype_menu.grid(row=2, column=1)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Login", command=self.login, bg="red", fg="white",
                  font=("Arial", 14, "bold"), width=15).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Signup", command=self.signup, bg="red", fg="white",
                  font=("Arial", 14, "bold"), width=15).pack(side="right", padx=10)

        self.root.mainloop()

    def toggle_password_visibility(self):
        if self.show_pass.get():
            self.pass_entry.config(show="")
        else:
            self.pass_entry.config(show="*")

    def login(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()
        usertype = self.usertype_var.get()

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT userid FROM user WHERE email=? AND password=? AND usertype=?", (email, password, usertype))
        result = cursor.fetchone()
        conn.close()

        if result:
            userid = result[0]
            self.root.destroy()
            if usertype == "jobseeker":
                JobSeekerWindow(userid)
            elif usertype == "employr":
                EmployerWindow(userid)
            elif usertype == "admin":
                AdminWindow(userid)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials or user type")

    def signup(self):
        from GUI.signup import SignupWindow
        self.root.destroy()
        SignupWindow()
