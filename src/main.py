from user import User
from seeker import JobSeeker
from Employer import Employer
from Vacancy_job import Vacancy
from Saved_Vacancy import SavedVacancy

# Initialize the shared base
base = User()







# Create a new vacancy by employer
vac = Vacancy()
vacancyid = vac.create_vacancy(
    employerid=1,
    title="Software Engineer",
    description="Entry-level Python developer position",
    location="Remote",
    industry="IT",
    salary=65000.00,
    requiredexperience="0-2 years",
    ishidden=False,
    dateposted="2025-05-15"
)

print(f"Vacancy created with ID = {vacancyid}")

# Save the vacancy by job seeker
sv = SavedVacancy()
sv.save_vacancy(seekerid=1, vacancyid=vacancyid)
#print(f"Vacancy {vacancyid} saved by seeker {}")

# Optional: List all saved vacancies for the seeker
saved_list = sv.list_saved(seekerid=1)
#print(f"Saved vacancies for seeker {seekerid}: {saved_list}")
