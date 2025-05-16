from user import User
from seeker import JobSeeker
from Employer import Employer
from Vacancy_job import Vacancy
from Saved_Vacancy import SavedVacancy
from Application import Application
from Application_details import ApplicationDetail
from GUI.login import LoginWindow



# Initialize the shared base
base = User()

app_detail = ApplicationDetail()



if __name__ == "__main__":
    LoginWindow()
