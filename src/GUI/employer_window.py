import tkinter as tk
import sqlite3

class EmployerWindow:
    def __init__(self, userid):
        self.userid = userid
        self.root = tk.Tk()
        self.root.title("Employer")
        self.root.geometry("700x500")
        self.root.configure(bg="black")

        # Fetch the employer's name from the database
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM user WHERE userid=?", (userid,))
        result = cursor.fetchone()
        conn.close()

        name = result[0] if result else "Unknown"

        tk.Label(self.root, text="Employer Dashboard", font=("Comic Sans MS", 28, "bold"),
                 fg="white", bg="black").pack(pady=30)

        info_frame = tk.Frame(self.root, bg="black")
        info_frame.pack(pady=10)

        tk.Label(info_frame, text=f"Welcome, {name}!", font=("Arial", 16, "bold"),
                 fg="white", bg="black").pack(pady=10)
        tk.Label(info_frame, text=f"User ID: {userid}", font=("Arial", 12),
                 fg="white", bg="black").pack(pady=5)

        # Add 6 red buttons: 3 on top row, 3 on bottom row
        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(pady=30)

        for i in range(1, 7):
            row = 0 if i <= 3 else 1
            col = (i - 1) % 3
            tk.Button(
                btn_frame,
                text=f"{i}",
                bg="red",
                fg="white",
                font=("Arial", 14, "bold"),
                width=10,
                height=2
            ).grid(row=row, column=col, padx=8, pady=8)

        self.root.mainloop()
