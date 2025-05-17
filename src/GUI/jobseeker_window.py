import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox
import sqlite3
from seeker import JobSeeker

class JobSeekerWindow:
    def __init__(self, userid):
        self.userid = userid
        self.root = tk.Tk()
        self.root.title("Job Seeker")
        self.root.geometry("700x500")
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
            text="5",
            bg="blue",
            fg="white",
            font=("Arial", 14, "bold"),
            width=15,
            height=2
        ).grid(row=1, column=1, padx=8, pady=8)

        # Button 6: Placeholder
        tk.Button(
            btn_frame,
            text="6",
            bg="blue",
            fg="white",
            font=("Arial", 14, "bold"),
            width=15,
            height=2
        ).grid(row=1, column=2, padx=8, pady=8)

        self.root.mainloop()

    def open_insert_info_window(self):
        insert_win = tk.Toplevel(self.root)
        insert_win.title("Insert Seeker Info")
        insert_win.geometry("400x300")
        insert_win.configure(bg="black")

        tk.Label(insert_win, text="Insert Your Info", font=("Arial", 16, "bold"),
                 fg="white", bg="black").pack(pady=10)

        form_frame = tk.Frame(insert_win, bg="black")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="CV (PDF):", bg="black", fg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        cv_path_var = tk.StringVar()
        cv_entry = tk.Entry(form_frame, font=("Arial", 12), width=25, textvariable=cv_path_var, state="readonly")
        cv_entry.grid(row=0, column=1, pady=5)

        def browse_cv():
            file_path = fd.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file_path:
                cv_path_var.set(file_path)

        tk.Button(form_frame, text="Browse", command=browse_cv, bg="blue", fg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5)

        tk.Label(form_frame, text="Experience Level:", bg="black", fg="white", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        exp_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        exp_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Industry:", bg="black", fg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
        industry_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        industry_entry.grid(row=2, column=1, pady=5)

        def save_info():
            cv_v = cv_path_var.get()
            experiencelevel = exp_entry.get()
            industry = industry_entry.get()
            seeker = JobSeeker()
            seeker.insert_seeker_info(self.userid, cv_v, experiencelevel, industry)
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

        tk.Label(form_frame, text="CV (PDF):", bg="black", fg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        cv_path_var = tk.StringVar()
        cv_entry = tk.Entry(form_frame, font=("Arial", 12), width=25, textvariable=cv_path_var, state="readonly")
        cv_entry.grid(row=0, column=1, pady=5)

        def browse_cv():
            file_path = fd.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file_path:
                cv_path_var.set(file_path)

        tk.Button(form_frame, text="Browse", command=browse_cv, bg="blue", fg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5)

        tk.Label(form_frame, text="Experience Level:", bg="black", fg="white", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        exp_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        exp_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Industry:", bg="black", fg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
        industry_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        industry_entry.grid(row=2, column=1, pady=5)

        def save_update():
            cv_v = cv_path_var.get()
            experiencelevel = exp_entry.get()
            industry = industry_entry.get()
            seeker = JobSeeker()
            seeker.insert_seeker_info(self.userid, cv_v, experiencelevel, industry)
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

        tk.Label(form_frame, text="New Email:", bg="black", fg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        email_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        email_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="New Password:", bg="black", fg="white", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        password_entry = tk.Entry(form_frame, font=("Arial", 12), width=25, show="*")
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
                messagebox.showinfo("Success", "Email/Password updated successfully!")
            else:
                messagebox.showwarning("No Change", "Please enter new email or password.")
            edit_win.destroy()

        tk.Button(edit_win, text="Save", command=save_email_password, bg="blue", fg="white",
                  font=("Arial", 12, "bold"), width=10).pack(pady=15)

    def open_vacancy_window(self):
        vacancy_win = tk.Toplevel(self.root)
        vacancy_win.title("Available Vacancies")
        vacancy_win.geometry("500x400")
        vacancy_win.configure(bg="black")

        tk.Label(vacancy_win, text="Available Vacancies", font=("Comic Sans MS", 20, "bold"),
                 fg="white", bg="black").pack(pady=20)

        vacancy_list_frame = tk.Frame(vacancy_win, bg="black")
        vacancy_list_frame.pack(pady=10, fill="both", expand=True)

        tk.Label(vacancy_list_frame, text="(Vacancy list goes here)", font=("Arial", 14),
                 fg="white", bg="black").pack(pady=10)
