

CREATE TABLE IF NOT EXISTS people (
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone_number VARCHAR(50),
    address VARCHAR(50),
    country VARCHAR(30),
    date_of_birth TIMESTAMP,
    passport_number VARCHAR(20) PRIMARY KEY,
    email VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(30) PRIMARY KEY,
    event_time TIMESTAMP,
    user_agent VARCHAR(100),
    person_passport_number VARCHAR(20) REFERENCES people,
);