import tkinter as tk
from tkinter import messagebox
import sqlite3

class SignupWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Signup")
        self.root.geometry("700x500")
        self.root.configure(bg="black")

        tk.Label(self.root, text="Create Account", font=("Comic Sans MS", 28, "bold"),
                 fg="white", bg="black").pack(pady=20)

        form_frame = tk.Frame(self.root, bg="black")
        form_frame.pack()

        labels = ["Email", "Password", "Name", "Location", "User Type", "Phone Number", "Date of Birth", "Age"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", bg="black", fg="white", font=("Arial", 12)).grid(row=i, column=0, sticky="e", pady=5, padx=10)
            if label == "User Type":
                self.usertype_var = tk.StringVar(value="jobseeker")
                dropdown = tk.OptionMenu(form_frame, self.usertype_var, "jobseeker", "employer", "admin")
                dropdown.config(font=("Arial", 12), bg="white")
                dropdown.grid(row=i, column=1, padx=10)
            else:
                entry = tk.Entry(form_frame, font=("Arial", 12), width=30, show="*" if label == "Password" else None)
                entry.grid(row=i, column=1, padx=10)
                self.entries[label] = entry

                # Show password checkbox
                if label == "Password":
                    self.show_pass = tk.BooleanVar()
                    tk.Checkbutton(form_frame, text="Show", variable=self.show_pass,
                                   command=self.toggle_signup_password_visibility,
                                   bg="black", fg="white").grid(row=i, column=2, padx=5)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Signup", command=self.signup_user, bg="red", fg="white",
                  font=("Arial", 14, "bold"), width=15).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Back to Login", command=self.back_to_login, bg="red", fg="white",
                  font=("Arial", 14, "bold"), width=15).pack(side="right", padx=10)

        self.root.mainloop()

    def toggle_signup_password_visibility(self):
        if self.show_pass.get():
            self.entries["Password"].config(show="")
        else:
            self.entries["Password"].config(show="*")

    def signup_user(self):
        email = self.entries["Email"].get()
        password = self.entries["Password"].get()
        name = self.entries["Name"].get()
        location = self.entries["Location"].get()
        usertype = self.usertype_var.get()
        phonenum = self.entries["Phone Number"].get()
        dob = self.entries["Date of Birth"].get()
        age = self.entries["Age"].get()

        if not (email and password and usertype):
            messagebox.showerror("Error", "Email, Password, and User Type are required")
            return

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO user (email, password, name, location, usertype, phonenum, dob, age)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (email, password, name, location, usertype, phonenum, dob, age))

            userid = cursor.lastrowid
            # Insert into jobseeker or employer table
            if usertype == "jobseeker":
                cursor.execute("""
                INSERT INTO jobseeker (userid, cv_v, experiencelevel, industry)
                VALUES (?, ?, ?, ?)""", (userid, b'', '', ''))
            elif usertype == "employer":
                cursor.execute("""
                INSERT INTO employer (userid, company_name, company_description, industry)
                VALUES (?, ?, ?, ?)""", (userid, '', '', ''))
            elif usertype == "admin":
                pass

            conn.commit()

            messagebox.showinfo("Success", f"{usertype.capitalize()} signed up successfully!")
            self.root.destroy()
            from GUI.login import LoginWindow
            LoginWindow()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists!")
        finally:
            conn.close()

    def back_to_login(self):
        self.root.destroy()
        from GUI.login import LoginWindow
        LoginWindow()
