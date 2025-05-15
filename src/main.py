from user import User
from seeker import JobSeeker
from Employer import Employer

# Initialize the shared base
base = User()

# Create first user (Job Seeker)
userid_seeker = base.signup_user(
    email="seeker2@example.com",
    password="seekpass",
    name="Alice",
    location="New York",
    usertype="jobseeker",
    phonenum="1234567890",
    dob="1995-05-05",
    age=29
)

# Create second user (Employer)
userid_employer = base.signup_user(
    email="employer303@example.com",
    password="emppass",
    name="Bob",
    location="San Francisco",
    usertype="employer",
    phonenum="9876543210",
    dob="1980-01-01",
    age=45
)

# Now use JobSeeker class to add extra info for the jobseeker
js = JobSeeker()
js.cursor.execute("""
    INSERT INTO jobseeker (userid, cv_v, experiencelevel, industry)
    VALUES (?, ?, ?, ?)""",
    (userid_seeker, b"SampleCV", "Junior", "IT"))
js.conn.commit()

# Use Employer class to add extra info for the employer
emp = Employer()
emp.cursor.execute("""
    INSERT INTO employer (userid, company_name, company_description, industry)
    VALUES (?, ?, ?, ?)""",
    (userid_employer, "Tech Corp", "A tech-focused company", "Technology"))
emp.conn.commit()

print(f"Job Seeker user created with userid = {userid_seeker}")
print(f"Employer user created with userid = {userid_employer}")
