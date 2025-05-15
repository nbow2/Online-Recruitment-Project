import sqlite3
import tkinter as tk
from tkinter import messagebox

class User:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self._create_users_table()

    def _create_users_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            role TEXT NOT NULL)''')
        conn.commit()
        conn.close()

    def signup(self, username, password, role):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, password, role))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None


class GUI:
    def __init__(self, root):
        self.user = User()
        self.root = root
        self.root.title("User Authentication")
        self.create_login_screen()

    def create_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.handle_login).pack(pady=5)
        tk.Button(self.root, text="Signup", command=self.create_signup_screen).pack()

    def create_signup_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Signup", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Label(self.root, text="Role:").pack()
        self.role_var = tk.StringVar(value="Job Seeker")
        tk.Radiobutton(self.root, text="Job Seeker", variable=self.role_var, value="Job Seeker").pack()
        tk.Radiobutton(self.root, text="Employer", variable=self.role_var, value="Employer").pack()

        tk.Button(self.root, text="Signup", command=self.handle_signup).pack(pady=5)
        tk.Button(self.root, text="Back to Login", command=self.create_login_screen).pack()

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.user.login(username, password)
        if role:
            messagebox.showinfo("Login Successful", f"Welcome, {username}! You are logged in as a {role}.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def handle_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        if self.user.signup(username, password, role):
            messagebox.showinfo("Signup Successful", "Your account has been created. Please log in.")
            self.create_login_screen()
        else:
            messagebox.showerror("Signup Failed", "Username already exists. Please choose a different username.")


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()