import tkinter as tk

class JobSeekerWindow:
    def __init__(self, userid):
        self.userid = userid
        self.root = tk.Tk()
        self.root.title("JOB Seeker")

        label = tk.Label(self.root, text=f"Welcome Job Seeker (User ID: {userid})", font=("Arial", 16))
        label.pack(padx=20, pady=20)

        self.root.mainloop()
