import tkinter as tk

class EmployerWindow:
    def __init__(self, userid):
        self.userid = userid
        self.root = tk.Tk()
        self.root.title("EMPLOYER")

        label = tk.Label(self.root, text=f"Welcome Employer (User ID: {userid})", font=("Arial", 16))
        label.pack(padx=20, pady=20)

        self.root.mainloop()
