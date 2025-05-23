-- Users table
CREATE TABLE [user] (
    userid INT PRIMARY KEY IDENTITY(1,1),
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    location VARCHAR(255),
    usertype VARCHAR(100) CHECK (usertype IN ('jobseeker', 'employer')),
    phonenum VARCHAR(100),
    dob VARCHAR(100),
    age INT
);

-- Job seeker table
CREATE TABLE jobseeker (
    seekerid INT PRIMARY KEY IDENTITY(1,1),
    userid INT NOT NULL,
    cv_v VARBINARY(MAX),
    experiencelevel VARCHAR(100),
    industry VARCHAR(100),
    FOREIGN KEY (userid) REFERENCES [user](userid)
);

-- Employer table
CREATE TABLE employer (
    employerid INT PRIMARY KEY IDENTITY(1,1),
    userid INT NOT NULL,
    company_name VARCHAR(255),
    company_description VARCHAR(255),
    industry VARCHAR(100),
    FOREIGN KEY (userid) REFERENCES [user](userid)
);

-- Vacancy table
CREATE TABLE vacancy (
    vacancyid INT PRIMARY KEY IDENTITY(1,1),
    employerid INT NOT NULL,
    title VARCHAR(255),
    description TEXT,
    location VARCHAR(255),
    industry VARCHAR(100),
    salary DECIMAL(10,3),
    requiredexperience VARCHAR(255),
    ishidden BIT DEFAULT 0,
    dateposted VARCHAR(100),
    FOREIGN KEY (employerid) REFERENCES employer(employerid)
);

-- Application table
CREATE TABLE application (
    applicationid INT PRIMARY KEY IDENTITY(1,1),
    seekerid INT NOT NULL,
    vacancyid INT NOT NULL,
    dateapplied VARCHAR(255),
    industry VARCHAR(100),
    FOREIGN KEY (seekerid) REFERENCES jobseeker(seekerid),
    FOREIGN KEY (vacancyid) REFERENCES vacancy(vacancyid)
);

-- SavedVacancy table
CREATE TABLE savedvacancy (
    seekerid INT,
    vacancyid INT,
    datesaved DATE DEFAULT GETDATE(),
    PRIMARY KEY (seekerid, vacancyid),
    FOREIGN KEY (seekerid) REFERENCES jobseeker(seekerid),
    FOREIGN KEY (vacancyid) REFERENCES vacancy(vacancyid)
);

-- ApplicationDetail table
CREATE TABLE applicationdetail (
    detailid INT PRIMARY KEY IDENTITY(1,1),
    applicationid INT NOT NULL,
    coverletter VARCHAR(255),
    interviewnotes VARCHAR(255),
    reviewstatus VARCHAR(50) CHECK (reviewstatus IN ('Pending', 'Reviewed', 'Shortlisted', 'Rejected')),
    reviewerid INT,
    lastupdated DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (applicationid) REFERENCES application(applicationid),
    FOREIGN KEY (reviewerid) REFERENCES employer(employerid)
);

