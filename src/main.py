from user import User
from seeker import JobSeeker
from Employer import Employer
from Vacancy_job import Vacancy
from Saved_Vacancy import SavedVacancy
from Application import Application
from Application_details import ApplicationDetail


# Initialize the shared base
base = User()

app_detail = ApplicationDetail()

details = app_detail.get_full_details()
for row in details:
    print("\n--- Application Detail ---")
    print(f"Detail ID       : {row[0]}")
    print(f"Application ID  : {row[1]}")
    print(f"Seeker Name     : {row[2]}")
    print(f"Vacancy Title   : {row[3]}")
    print(f"Cover Letter    : {row[4]}")
    print(f"Interview Notes : {row[5]}")
    print(f"Review Status   : {row[6]}")
    print(f"Reviewer Name   : {row[7]}")
    print(f"Last Updated    : {row[8]}")
