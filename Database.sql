-- Bảng User
CREATE TABLE User (
    us_id VARCHAR(20) PRIMARY KEY,
    us_name VARCHAR(100),
    us_email VARCHAR(100),
    us_password VARCHAR(100),
    us_img VARCHAR(255)
);

-- Bảng Verification
CREATE TABLE Verification (
    us_id VARCHAR(20),
    vc_otp VARCHAR(20),
    vc_start DATE,
    vc_end DATE,
    vc_status BOOLEAN,
    FOREIGN KEY (us_id) REFERENCES User(us_id)
);

-- Bảng WorkSpace
CREATE TABLE WorkSpace (
    ws_id VARCHAR(20) PRIMARY KEY,
    ws_name VARCHAR(100),
    us_id VARCHAR(20),
    FOREIGN KEY (us_id) REFERENCES User(us_id)
);

-- Bảng InSpace
CREATE TABLE InSpace (
    is_id VARCHAR(20) PRIMARY KEY,
    is_role VARCHAR(50),
    ws_id VARCHAR(20),
    us_id VARCHAR(20),
    FOREIGN KEY (ws_id) REFERENCES WorkSpace(ws_id),
    FOREIGN KEY (us_id) REFERENCES User(us_id)
);

-- Bảng Note
CREATE TABLE Note (
    nt_id VARCHAR(20) PRIMARY KEY,
    nt_title VARCHAR(100),
    nt_subtitle VARCHAR(100),
    nt_content TEXT,
    nt_img VARCHAR(255),
    nt_pdf VARCHAR(255),
    nt_date DATETIME,
    us_id VARCHAR(20),
    FOREIGN KEY (us_id) REFERENCES User(us_id)
);

-- Bảng Task
CREATE TABLE Task (
    ts_id VARCHAR(20) PRIMARY KEY,
    ts_title VARCHAR(100),
    ts_subtitle VARCHAR(100),
    ts_status BOOLEAN,
    ts_start DATE,
    ts_end DATE,
    ts_note TEXT,
    us_id VARCHAR(20),
    ws_id VARCHAR(20),
    FOREIGN KEY (us_id) REFERENCES User(us_id),
    FOREIGN KEY (ws_id) REFERENCES WorkSpace(ws_id)
);

-- Bảng Subtask
CREATE TABLE Subtask (
    st_id VARCHAR(20) PRIMARY KEY,
    st_title VARCHAR(100),
    st_subtitle VARCHAR(100),
    st_note TEXT,
    st_status BOOLEAN,
    st_start DATE,
    st_end DATE,
    us_id VARCHAR(20),
    ts_id VARCHAR(20),
    FOREIGN KEY (us_id) REFERENCES User(us_id),
    FOREIGN KEY (ts_id) REFERENCES Task(ts_id)
);

-- Bảng Todo
CREATE TABLE Todo (
    td_id VARCHAR(20) PRIMARY KEY,
    td_type VARCHAR(100),
    td_status BOOLEAN,
    st_id VARCHAR(20),
    ts_id VARCHAR(20),
    FOREIGN KEY (st_id) REFERENCES Subtask(st_id),
    FOREIGN KEY (ts_id) REFERENCES Task(ts_id)
);

-- Bảng UsedTask
CREATE TABLE UsedTask (
    ut_id VARCHAR(20) PRIMARY KEY,
    us_id VARCHAR(20),
    ts_id VARCHAR(20),
    FOREIGN KEY (us_id) REFERENCES User(us_id),
    FOREIGN KEY (ts_id) REFERENCES Task(ts_id)
);