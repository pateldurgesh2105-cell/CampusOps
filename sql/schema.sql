CREATE TABLE complaints (
    complaint_id VARCHAR(20) PRIMARY KEY,
    created_date DATE NOT NULL,
    building VARCHAR(80),
    room_no INT,
    category VARCHAR(50),
    description TEXT,
    department VARCHAR(80),
    priority VARCHAR(20),
    status VARCHAR(30),
    resolution_days NUMERIC
);

CREATE TABLE energy_usage (
    date DATE,
    building VARCHAR(80),
    energy_kwh NUMERIC
);

CREATE TABLE equipment (
    equipment_id VARCHAR(20) PRIMARY KEY,
    building VARCHAR(80),
    equipment_type VARCHAR(50),
    brand VARCHAR(50),
    status VARCHAR(50),
    installed_date DATE
);
