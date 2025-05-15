-- Users table
CREATE TABLE user (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    location VARCHAR(255),
    usertype VARCHAR(100) CHECK (usertype IN ('jobseeker', 'employer')),
    phonenum VARCHAR(100),
    dob VARCHAR(100),
    age INTEGER
);

-- Job seeker table
CREATE TABLE jobseeker (
    seekerid INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    cv_v BLOB,
    experiencelevel VARCHAR(100),
    industry VARCHAR(100),
    FOREIGN KEY (userid) REFERENCES user(userid)
);

-- Employer table
CREATE TABLE employer (
    employerid INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    company_name VARCHAR(255),
    company_description VARCHAR(255),
    industry VARCHAR(100),
    FOREIGN KEY (userid) REFERENCES user(userid)
);

-- Vacancy table
CREATE TABLE vacancy (
    vacancyid INTEGER PRIMARY KEY AUTOINCREMENT,
    employerid INTEGER NOT NULL,
    title VARCHAR(255),
    description TEXT,
    location VARCHAR(255),
    industry VARCHAR(100),
    salary DECIMAL(10,3),
    requiredexperience VARCHAR(255),
    ishidden BOOLEAN DEFAULT FALSE,
    dateposted VARCHAR(100),
    FOREIGN KEY (employerid) REFERENCES employer(employerid)
);

-- Application table
CREATE TABLE application (
    applicationid INTEGER PRIMARY KEY AUTOINCREMENT,
    seekerid INTEGER NOT NULL,
    vacancyid INTEGER NOT NULL,
    dateapplied VARCHAR(255),
    industry VARCHAR(100),
    FOREIGN KEY (seekerid) REFERENCES jobseeker(seekerid),
    FOREIGN KEY (vacancyid) REFERENCES vacancy(vacancyid)
);

-- SavedVacancy table
CREATE TABLE savedvacancy (
    seekerid INTEGER,
    vacancyid INTEGER,
    datesaved DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (seekerid, vacancyid),
    FOREIGN KEY (seekerid) REFERENCES jobseeker(seekerid),
    FOREIGN KEY (vacancyid) REFERENCES vacancy(vacancyid)
);

-- ApplicationDetail table
CREATE TABLE applicationdetail (
    detailid INTEGER PRIMARY KEY AUTOINCREMENT,
    applicationid INTEGER NOT NULL,
    coverletter VARCHAR(255),
    interviewnotes VARCHAR(255),
    reviewstatus TEXT CHECK (reviewstatus IN ('Pending', 'Reviewed', 'Shortlisted', 'Rejected')),
    reviewerid INTEGER,
    lastupdated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (applicationid) REFERENCES application(applicationid),
    FOREIGN KEY (reviewerid) REFERENCES employer(employerid)
);
