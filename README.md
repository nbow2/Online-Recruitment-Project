# Online Recruitment Project

This is an online recruitment management system built with Python and SQLite, featuring a Tkinter GUI for job seekers, employers, and admins.

## Features

- User registration and login (Jobseeker, Employer, Admin)
- Jobseeker profile management, CV upload, job search, application, and saved jobs
- Employer job posting, vacancy management, application review, and company profile editing
- Admin dashboard for user and vacancy management, analytics, and reporting
- Analytics: most applied job, jobs with no applicants, top employer, industry report
- Data stored in SQLite database (`db.sqlite3`)

## Project Structure

```
db.sqlite3
Recruitment.sql
diagrams/
src/
    admin.py
    analytics.py
    Application_details.py
    Application.py
    Employer.py
    main.py
    operations.py
    Saved_Vacancy.py
    seeker.py
    server_con.py
    user.py
    Vacancy_job.py
    GUI/
        login.py
        signup.py
        jobseeker_window.py
        employer_window.py
        admin_window.py
```

## Getting Started

1. **Install requirements**  
   This project uses only Python standard libraries (Tkinter, sqlite3).

2. **Initialize the database**  
   The database (`db.sqlite3`) is created automatically if it doesn't exist.  
   To reset or manually create tables, run:
   ```sh
   python src/server_con.py
   ```

3. **Run the application**  
   Start the GUI:
   ```sh
   python src/main.py
   ```

4. **Login or Signup**  
   Use the GUI to create accounts and access features based on your user type.

## Database Schema

- See [`Recruitment.sql`](Recruitment.sql) for the full schema.
- ER diagrams are available in the `diagrams/` folder.

## Notes

- All data is stored locally in `db.sqlite3`.
- The GUI is built with Tkinter and runs on Python 3.x.

## Authors

- Ahmed Dafalla
- Ahmed bandar bin khunfur
