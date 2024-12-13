-- YMS_db 데이터베이스 생성 및 선택
CREATE DATABASE IF NOT EXISTS YMS_db;
USE YMS_db;

-- 사용자에게 권한 부여
GRANT ALL PRIVILEGES ON YMS_db.* TO 'user'@'%';

-- 변경 사항 적용
FLUSH PRIVILEGES;

-- Address 테이블 생성
CREATE TABLE Address (
    Address_ID INT NOT NULL AUTO_INCREMENT,
    House_Number VARCHAR(20) NULL,
    Street_Name VARCHAR(20) NULL,
    City VARCHAR(20) NULL,
    ZipCode INT NULL,
    PRIMARY KEY (Address_ID)
);

-- Division 테이블 생성
CREATE TABLE Division (
    Division_ID VARCHAR(10) NOT NULL,
    Division_Name VARCHAR(30) NOT NULL,
    Address_ID INT NOT NULL,
    PRIMARY KEY (Division_ID),
    FOREIGN KEY (Address_ID) REFERENCES Address(Address_ID)
);

-- Yard 테이블 생성
CREATE TABLE Yard (
    Yard_ID VARCHAR(20) NOT NULL,
    Division_ID VARCHAR(10) NOT NULL,
    Yard_Name VARCHAR(30) NOT NULL,
    Site_ID VARCHAR(20) NULL,
    Address_ID INT NOT NULL,
    PRIMARY KEY (Yard_ID),
    FOREIGN KEY (Division_ID) REFERENCES Division(Division_ID),
    FOREIGN KEY (Address_ID) REFERENCES Address(Address_ID)
);

-- Site 테이블 생성
CREATE TABLE Site (
    Site_ID VARCHAR(20) NOT NULL,
    Yard_ID VARCHAR(20) NOT NULL,
    Site_Name VARCHAR(30) NULL,
    Storage_Type VARCHAR(20) NULL,
    Address_ID INT NOT NULL,
    y_Cordinate INT NULL,
    x_Cordinate INT NULL,
    y_Max_Size INT NULL,
    x_Max_Size INT NULL,
    PRIMARY KEY (Site_ID),
    FOREIGN KEY (Yard_ID) REFERENCES Yard(Yard_ID),
    FOREIGN KEY (Address_ID) REFERENCES Address(Address_ID)
);

-- Zone 테이블 생성
CREATE TABLE Zone (
    Zone_ID VARCHAR(30) NOT NULL,
    Site_ID VARCHAR(20) NOT NULL,
    Status VARCHAR(20) NULL,
    y_Cordinate INT NULL,
    x_Cordinate INT NULL,
    PRIMARY KEY (Zone_ID),
    FOREIGN KEY (Site_ID) REFERENCES Site(Site_ID)
);

-- Truck 테이블 생성
CREATE TABLE Truck (
    Truck_ID VARCHAR(10) NOT NULL,
    Status VARCHAR(20) NULL,
    Zone_ID VARCHAR(30) NOT NULL,
    PRIMARY KEY (Truck_ID),
    FOREIGN KEY (Zone_ID) REFERENCES Zone(Zone_ID)
);

-- Chassis 테이블 생성
CREATE TABLE Chassis (
    Chassis_ID VARCHAR(10) NOT NULL,
    Status VARCHAR(20) NULL,
    Type VARCHAR(20) NULL,
    Truck_ID VARCHAR(10) NOT NULL,
    Zone_ID VARCHAR(30) NOT NULL,
    PRIMARY KEY (Chassis_ID),
    FOREIGN KEY (Truck_ID) REFERENCES Truck(Truck_ID),
    FOREIGN KEY (Zone_ID) REFERENCES Zone(Zone_ID)
);

-- Container 테이블 생성
CREATE TABLE Container (
    Container_ID VARCHAR(20) NOT NULL,
    Status VARCHAR(20) NULL,
    Chassis_ID VARCHAR(10) NOT NULL,
    Type VARCHAR(255) NULL,
    Size VARCHAR(255) NULL,
    Zone_ID VARCHAR(30) NOT NULL,
    PRIMARY KEY (Container_ID),
    FOREIGN KEY (Chassis_ID) REFERENCES Chassis(Chassis_ID),
    FOREIGN KEY (Zone_ID) REFERENCES Zone(Zone_ID)
);

-- Trailer 테이블 생성
CREATE TABLE Trailer (
    Trailer_ID VARCHAR(10) NOT NULL,
    Status VARCHAR(20) NULL,
    Type VARCHAR(20) NULL,
    Zone_ID VARCHAR(30) NOT NULL,
    Truck_ID VARCHAR(10) NOT NULL,
    PRIMARY KEY (Trailer_ID),
    FOREIGN KEY (Zone_ID) REFERENCES Zone(Zone_ID),
    FOREIGN KEY (Truck_ID) REFERENCES Truck(Truck_ID)
);

-- User 테이블 생성
CREATE TABLE User (
    User_ID VARCHAR(20) NOT NULL,
    UserName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NULL,
    Role_ID INT NULL,
    Phone_Number VARCHAR(20) NULL,
    PRIMARY KEY (User_ID)
);

-- Driver 테이블 생성
CREATE TABLE Driver (
    User_ID VARCHAR(20) NOT NULL,
    Current_Location VARCHAR(20) DEFAULT NULL,
    Current_Status VARCHAR(20) DEFAULT NULL,
    Private_Truck_Info VARCHAR(20) DEFAULT NULL,
    Truck_ID VARCHAR(10) DEFAULT 'T_0001',
    PRIMARY KEY (User_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (Truck_ID) REFERENCES Truck(Truck_ID)
);

-- Manager 테이블 생성
CREATE TABLE Manager (
    User_ID VARCHAR(20) NOT NULL,
    Position VARCHAR(50) DEFAULT NULL,
    Office_Phone VARCHAR(20) DEFAULT NULL,
    Division_ID VARCHAR(10) DEFAULT 'LA',
    PRIMARY KEY (User_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (Division_ID) REFERENCES Division(Division_ID)
);

-- Password 테이블 생성
CREATE TABLE Password (
    User_ID VARCHAR(20) NOT NULL,
    Password VARCHAR(255) NULL,
    PRIMARY KEY (User_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

-- Tranport_Log 테이블 생성
CREATE TABLE Transport_Log (
    Log_ID INT NOT NULL AUTO_INCREMENT,
    Driver_ID VARCHAR(20) NULL,
    Container_ID VARCHAR(20) NULL,
    Chassis_ID VARCHAR(10) NULL,
    Truck_ID VARCHAR(10) NULL,
    Trailer_ID VARCHAR(10) NULL,
    Depart_Zone_ID VARCHAR(30) NULL,
    Depart_Date DATE NULL,
    Arrive_Zone_ID VARCHAR(30)NULL,
    Arrive_Date DATE NULL,
    Assigned Boolean NULL,
    Log_Memo VARCHAR(200) NULL,
    PRIMARY KEY (Log_ID),
    FOREIGN KEY (Driver_ID) REFERENCES Driver(User_ID),
    FOREIGN KEY (Container_ID) REFERENCES Container(Container_ID),
    FOREIGN KEY (Chassis_ID) REFERENCES Chassis(Chassis_ID),
    FOREIGN KEY (Truck_ID) REFERENCES Truck(Truck_ID),
    FOREIGN KEY (Trailer_ID) REFERENCES Trailer(Trailer_ID),
    FOREIGN KEY (Depart_Zone_ID) REFERENCES Zone(Zone_ID),
    FOREIGN KEY (Arrive_Zone_ID) REFERENCES Zone(Zone_ID)
);

-- 테스트 데이터 삽입

-- Address 데이터 삽입
-- City는 Los Angeles, Phoenix, Houston, Savannah, Mobile이 끝임.
INSERT INTO Address (House_Number, Street_Name, City, ZipCode) VALUES
    ('100', 'Main St', 'Los Angeles', 90001),
    ('200', '2nd Ave', 'Phoenix', 85001),
    ('300', '3rd Blvd', 'Houston', 77001),
    ('400', '4th St', 'Savannah', 31401),
    ('500', '5th Ave', 'Mobile', 36601),
    ('600', '6th St', 'Los Angeles', 90002),
    ('700', '7th Ave', 'Phoenix', 85002),
    ('800', '8th Blvd', 'Houston', 77002),
    ('900', '9th Dr', 'Savannah', 31402),
    ('1000', '10th Ct', 'Mobile', 36602);

-- Division 데이터 삽입
-- Division은 여기 5개가 끝임. 추가할 필요 없음.
INSERT INTO Division (Division_ID, Division_Name, Address_ID) VALUES
    ('LA', 'Los Angeles', 1),
    ('PHX', 'Phoenix', 2),
    ('HOU', 'Houston', 3),
    ('SAV', 'Savannah', 4),
    ('MOB', 'Mobile', 5);

-- Yard 데이터 삽입
-- Yard는 같은 division 안에 여러 곳이 있을 수 있음. Yard마다 다른 주소를 가짐.
INSERT INTO Yard (Yard_ID, Division_ID, Yard_Name, Site_ID, Address_ID) VALUES
    ('HOU_YARD_0001', 'HOU', 'Yard 1 HOU', 'HOU_SITE_0001', 3),
    ('LA_YARD_0001', 'LA', 'Yard 1 LA', 'LA_SITE_0001', 1),
    ('MOB_YARD_0001', 'MOB', 'Yard 1 MOB', 'MOB_SITE_0001', 5),
    ('PHX_YARD_0001', 'PHX', 'Yard 1 PHX', 'PHX_SITE_0001', 2),
    ('SAV_YARD_0001', 'SAV', 'Yard 1 SAV', 'SAV_SITE_0001', 4),
    ('HOU_YARD_0002', 'HOU', 'Yard 2 HOU', 'HOU_SITE_0002', 8),
    ('LA_YARD_0002', 'LA', 'Yard 2 LA', 'LA_SITE_0002', 6),
    ('MOB_YARD_0002', 'MOB', 'Yard 2 MOB', 'MOB_SITE_0002', 10),
    ('PHX_YARD_0002', 'PHX', 'Yard 2 PHX', 'PHX_SITE_0002', 7),
    ('SAV_YARD_0002', 'SAV', 'Yard 2 SAV', 'SAV_SITE_0002', 9);

-- Site 데이터 삽입
-- Yard안에 최소 4개의 Site: Truck, Chassis, Container, Trailer
INSERT INTO Site (Site_ID, Yard_ID, Site_Name, Storage_Type, Address_ID, y_Cordinate, x_Cordinate, y_Max_Size, x_Max_Size) VALUES
    -- HOU_YARD_0001
    ('HOU_SITE_0001', 'HOU_YARD_0001', 'Site 1 HOU', 'Truck', 3, 0, 0, 100, 100),
    ('HOU_SITE_0002', 'HOU_YARD_0001', 'Site 2 HOU', 'Chassis', 3, 1, 1, 100, 100),
    ('HOU_SITE_0003', 'HOU_YARD_0001', 'Site 3 HOU', 'Container', 3, 2, 2, 100, 100),
    ('HOU_SITE_0004', 'HOU_YARD_0001', 'Site 4 HOU', 'Trailer', 3, 3, 3, 100, 100),
    -- HOU_YARD_0002
    ('HOU_SITE_0005', 'HOU_YARD_0002', 'Site 1 HOU 2', 'Truck', 6, 0, 0, 100, 100),
    ('HOU_SITE_0006', 'HOU_YARD_0002', 'Site 2 HOU 2', 'Chassis', 6, 1, 1, 100, 100),
    ('HOU_SITE_0007', 'HOU_YARD_0002', 'Site 3 HOU 2', 'Container', 6, 2, 2, 100, 100),
    ('HOU_SITE_0008', 'HOU_YARD_0002', 'Site 4 HOU 2', 'Trailer', 6, 3, 3, 100, 100),
    -- LA_YARD_0001
    ('LA_SITE_0001', 'LA_YARD_0001', 'Site 1 LA', 'Truck', 1, 0, 0, 100, 100),
    ('LA_SITE_0002', 'LA_YARD_0001', 'Site 2 LA', 'Chassis', 1, 1, 1, 100, 100),
    ('LA_SITE_0003', 'LA_YARD_0001', 'Site 3 LA', 'Container', 1, 2, 2, 100, 100),
    ('LA_SITE_0004', 'LA_YARD_0001', 'Site 4 LA', 'Trailer', 1, 3, 3, 100, 100),
    -- LA_YARD_0002
    ('LA_SITE_0005', 'LA_YARD_0002', 'Site 1 LA 2', 'Truck', 7, 0, 0, 100, 100),
    ('LA_SITE_0006', 'LA_YARD_0002', 'Site 2 LA 2', 'Chassis', 7, 1, 1, 100, 100),
    ('LA_SITE_0007', 'LA_YARD_0002', 'Site 3 LA 2', 'Container', 7, 2, 2, 100, 100),
    ('LA_SITE_0008', 'LA_YARD_0002', 'Site 4 LA 2', 'Trailer', 7, 3, 3, 100, 100),
    -- PHX_YARD_0001
    ('PHX_SITE_0001', 'PHX_YARD_0001', 'Site 1 PHX', 'Truck', 2, 0, 0, 100, 100),
    ('PHX_SITE_0002', 'PHX_YARD_0001', 'Site 2 PHX', 'Chassis', 2, 1, 1, 100, 100),
    ('PHX_SITE_0003', 'PHX_YARD_0001', 'Site 3 PHX', 'Container', 2, 2, 2, 100, 100),
    ('PHX_SITE_0004', 'PHX_YARD_0001', 'Site 4 PHX', 'Trailer', 2, 3, 3, 100, 100),
    -- PHX_YARD_0002
    ('PHX_SITE_0005', 'PHX_YARD_0002', 'Site 1 PHX 2', 'Truck', 8, 0, 0, 100, 100),
    ('PHX_SITE_0006', 'PHX_YARD_0002', 'Site 2 PHX 2', 'Chassis', 8, 1, 1, 100, 100),
    ('PHX_SITE_0007', 'PHX_YARD_0002', 'Site 3 PHX 2', 'Container', 8, 2, 2, 100, 100),
    ('PHX_SITE_0008', 'PHX_YARD_0002', 'Site 4 PHX 2', 'Trailer', 8, 3, 3, 100, 100),
    -- SAV_YARD_0001
    ('SAV_SITE_0001', 'SAV_YARD_0001', 'Site 1 SAV', 'Truck', 4, 0, 0, 100, 100),
    ('SAV_SITE_0002', 'SAV_YARD_0001', 'Site 2 SAV', 'Chassis', 4, 1, 1, 100, 100),
    ('SAV_SITE_0003', 'SAV_YARD_0001', 'Site 3 SAV', 'Container', 4, 2, 2, 100, 100),
    ('SAV_SITE_0004', 'SAV_YARD_0001', 'Site 4 SAV', 'Trailer', 4, 3, 3, 100, 100),
    -- SAV_YARD_0002
    ('SAV_SITE_0005', 'SAV_YARD_0002', 'Site 1 SAV 2', 'Truck', 9, 0, 0, 100, 100),
    ('SAV_SITE_0006', 'SAV_YARD_0002', 'Site 2 SAV 2', 'Chassis', 9, 1, 1, 100, 100),
    ('SAV_SITE_0007', 'SAV_YARD_0002', 'Site 3 SAV 2', 'Container', 9, 2, 2, 100, 100),
    ('SAV_SITE_0008', 'SAV_YARD_0002', 'Site 4 SAV 2', 'Trailer', 9, 3, 3, 100, 100),
    -- MOB_YARD_0001
    ('MOB_SITE_0001', 'MOB_YARD_0001', 'Site 1 MOB', 'Truck', 5, 0, 0, 100, 100),
    ('MOB_SITE_0002', 'MOB_YARD_0001', 'Site 2 MOB', 'Chassis', 5, 1, 1, 100, 100),
    ('MOB_SITE_0003', 'MOB_YARD_0001', 'Site 3 MOB', 'Container', 5, 2, 2, 100, 100),
    ('MOB_SITE_0004', 'MOB_YARD_0001', 'Site 4 MOB', 'Trailer', 5, 3, 3, 100, 100),
    -- MOB_YARD_0002
    ('MOB_SITE_0005', 'MOB_YARD_0002', 'Site 1 MOB 2', 'Truck', 10, 0, 0, 100, 100),
    ('MOB_SITE_0006', 'MOB_YARD_0002', 'Site 2 MOB 2', 'Chassis', 10, 1, 1, 100, 100),
    ('MOB_SITE_0007', 'MOB_YARD_0002', 'Site 3 MOB 2', 'Container', 10, 2, 2, 100, 100),
    ('MOB_SITE_0008', 'MOB_YARD_0002', 'Site 4 MOB 2', 'Trailer', 10, 3, 3, 100, 100);

-- Zone 데이터 삽입
-- 하나의 site는 T_Zone, C_Zone, CT_Zone, TL_Zone을 각각 30개, 20개, 40개, 10개를 갖는다.
-- T_Zone 데이터 삽입 (특정 Site에서 30개씩, 번호 연속)
INSERT INTO Zone (Zone_ID, Site_ID, Status, y_Cordinate, x_Cordinate)
SELECT 
    CONCAT('T_ZONE_', LPAD((ROW_NUMBER() OVER (ORDER BY s.Site_ID, N.num) + IFNULL(MAX_ZONE.base_num, 0)), 4, '0')) AS Zone_ID,
    s.Site_ID,
    'Available' AS Status,
    FLOOR((N.num - 1) / 6) AS y_Cordinate,
    (N.num - 1) % 6 AS x_Cordinate
FROM Site s
CROSS JOIN (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
    UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
    UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20
    UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION SELECT 24 UNION SELECT 25
    UNION SELECT 26 UNION SELECT 27 UNION SELECT 28 UNION SELECT 29 UNION SELECT 30
) N
LEFT JOIN (
    SELECT MAX(CAST(SUBSTRING(Zone_ID, 8) AS UNSIGNED)) AS base_num
    FROM Zone
    WHERE Zone_ID LIKE 'T_ZONE_%'
) MAX_ZONE ON 1 = 1
WHERE s.Storage_Type = 'Truck'
  AND s.Site_ID IN ('HOU_SITE_0001', 'HOU_SITE_0005', 'LA_SITE_0001', 'LA_SITE_0005', 
                    'PHX_SITE_0001', 'PHX_SITE_0005', 'MOB_SITE_0001', 'MOB_SITE_0005', 
                    'SAV_SITE_0001', 'SAV_SITE_0005');

-- C_Zone 데이터 삽입 (특정 Site에서 20개씩, 번호 연속)
INSERT INTO Zone (Zone_ID, Site_ID, Status, y_Cordinate, x_Cordinate)
SELECT 
    CONCAT('C_ZONE_', LPAD((ROW_NUMBER() OVER (ORDER BY s.Site_ID, N.num) + IFNULL(MAX_ZONE.base_num, 0)), 4, '0')) AS Zone_ID,
    s.Site_ID,
    'Available' AS Status,
    FLOOR((N.num - 1) / 5) AS y_Cordinate,
    (N.num - 1) % 5 AS x_Cordinate
FROM Site s
CROSS JOIN (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
    UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
    UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20
) N
LEFT JOIN (
    SELECT MAX(CAST(SUBSTRING(Zone_ID, 8) AS UNSIGNED)) AS base_num
    FROM Zone
    WHERE Zone_ID LIKE 'C_ZONE_%'
) MAX_ZONE ON 1 = 1
WHERE s.Storage_Type = 'Chassis'
  AND s.Site_ID IN ('HOU_SITE_0002', 'HOU_SITE_0006', 'LA_SITE_0002', 'LA_SITE_0006', 
                    'PHX_SITE_0002', 'PHX_SITE_0006', 'MOB_SITE_0002', 'MOB_SITE_0006', 
                    'SAV_SITE_0002', 'SAV_SITE_0006');

-- CT_Zone 데이터 삽입 (특정 Site에서 40개씩, 번호 연속)
INSERT INTO Zone (Zone_ID, Site_ID, Status, y_Cordinate, x_Cordinate)
SELECT 
    CONCAT('CT_ZONE_', LPAD((ROW_NUMBER() OVER (ORDER BY s.Site_ID, N.num) + IFNULL(MAX_ZONE.base_num, 0)), 4, '0')) AS Zone_ID,
    s.Site_ID,
    'Available' AS Status,
    FLOOR((N.num - 1) / 10) AS y_Cordinate,
    (N.num - 1) % 10 AS x_Cordinate
FROM Site s
CROSS JOIN (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
    UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
    UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20
    UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION SELECT 24 UNION SELECT 25
    UNION SELECT 26 UNION SELECT 27 UNION SELECT 28 UNION SELECT 29 UNION SELECT 30
    UNION SELECT 31 UNION SELECT 32 UNION SELECT 33 UNION SELECT 34 UNION SELECT 35
    UNION SELECT 36 UNION SELECT 37 UNION SELECT 38 UNION SELECT 39 UNION SELECT 40
) N
LEFT JOIN (
    SELECT MAX(CAST(SUBSTRING(Zone_ID, 9) AS UNSIGNED)) AS base_num
    FROM Zone
    WHERE Zone_ID LIKE 'CT_ZONE_%'
) MAX_ZONE ON 1 = 1
WHERE s.Storage_Type = 'Container'
  AND s.Site_ID IN ('HOU_SITE_0003', 'HOU_SITE_0007', 'LA_SITE_0003', 'LA_SITE_0007', 
                    'PHX_SITE_0003', 'PHX_SITE_0007', 'MOB_SITE_0003', 'MOB_SITE_0007', 
                    'SAV_SITE_0003', 'SAV_SITE_0007');

-- TL_Zone 데이터 삽입 (특정 Site에서 10개씩, 번호 연속)
INSERT INTO Zone (Zone_ID, Site_ID, Status, y_Cordinate, x_Cordinate)
SELECT 
    CONCAT('TL_ZONE_', LPAD((ROW_NUMBER() OVER (ORDER BY s.Site_ID, N.num) + IFNULL(MAX_ZONE.base_num, 0)), 4, '0')) AS Zone_ID,
    s.Site_ID,
    'Available' AS Status,
    FLOOR((N.num - 1) / 3) AS y_Cordinate,
    (N.num - 1) % 3 AS x_Cordinate
FROM Site s
CROSS JOIN (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
) N
LEFT JOIN (
    SELECT MAX(CAST(SUBSTRING(Zone_ID, 9) AS UNSIGNED)) AS base_num
    FROM Zone
    WHERE Zone_ID LIKE 'TL_ZONE_%'
) MAX_ZONE ON 1 = 1
WHERE s.Storage_Type = 'Trailer'
  AND s.Site_ID IN ('HOU_SITE_0004', 'HOU_SITE_0008', 'LA_SITE_0004', 'LA_SITE_0008', 
                    'PHX_SITE_0004', 'PHX_SITE_0008', 'MOB_SITE_0004', 'MOB_SITE_0008', 
                    'SAV_SITE_0004', 'SAV_SITE_0008');

-- User 테이블에 Driver 관련 데이터 삽입
INSERT INTO User (User_ID, UserName, Email, Role_ID, Phone_Number)
SELECT 
    CONCAT('driver', LPAD(t.num, 3, '0')) AS User_ID,
    CONCAT('Driver ', t.num) AS UserName,
    CONCAT('driver', t.num, '@example.com') AS Email,
    2 AS Role_ID, -- Role_ID 2는 Driver를 의미한다고 가정
    CONCAT('123-456-78', LPAD(t.num, 2, '0')) AS Phone_Number
FROM (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6
) t;
-- User 테이블에 Manager 관련 데이터 삽입
INSERT INTO User (User_ID, UserName, Email, Role_ID, Phone_Number)
SELECT 
    CONCAT('manager', LPAD(t.num, 3, '0')) AS User_ID,
    CONCAT('Manager ', t.num) AS UserName,
    CONCAT('manager', t.num, '@example.com') AS Email,
    1 AS Role_ID, -- Role_ID 1은 Manager를 의미한다고 가정
    CONCAT('123-456-78', LPAD(t.num, 2, '0')) AS Phone_Number
FROM (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
) t;

-- Truck 데이터 삽입
INSERT INTO Truck (Truck_ID, Status, Zone_ID)
SELECT 
    CONCAT('T_', LPAD(t.num, 4, '0')) AS Truck_ID,
    CASE WHEN t.num % 2 = 0 THEN 'Available' ELSE 'In Use' END AS Status,
    CONCAT('T_ZONE_', LPAD(t.num, 4, '0')) AS Zone_ID
FROM (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6
    UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12
    UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 UNION SELECT 16 UNION SELECT 17 UNION SELECT 18
    UNION SELECT 19 UNION SELECT 20 UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION SELECT 24
    UNION SELECT 25 UNION SELECT 26 UNION SELECT 27 UNION SELECT 28 UNION SELECT 29 UNION SELECT 30
) t;

-- Chassis 데이터 삽입
INSERT INTO Chassis (Chassis_ID, Status, Type, Truck_ID, Zone_ID)
SELECT 
    CONCAT('C_', LPAD(t.num, 4, '0')) AS Chassis_ID,
    CASE WHEN t.num % 2 = 0 THEN 'Available' ELSE 'In Use' END AS Status,
    CASE 
        WHEN t.num % 3 = 0 THEN 'Regular'
        WHEN t.num % 3 = 1 THEN 'Light'
        ELSE 'Tandem'
    END AS Type,
    CONCAT('T_', LPAD(t.num, 4, '0')) AS Truck_ID,
    CONCAT('C_ZONE_', LPAD(t.num, 4, '0')) AS Zone_ID
FROM (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6
    UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12
    UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 UNION SELECT 16 UNION SELECT 17 UNION SELECT 18
    UNION SELECT 19 UNION SELECT 20 UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION SELECT 24
    UNION SELECT 25 UNION SELECT 26 UNION SELECT 27 UNION SELECT 28 UNION SELECT 29 UNION SELECT 30
) t;

-- Regular 섀시는 20ST, 40ST 컨테이너를 운송할 수 있음
-- Light 섀시는 20ST 컨테이너를 운송할 수 있음
-- Tandem 섀시는 40HC, 45HC 컨테이너를 운송할 수 있음
-- ISO Tank, Flat Rack 컨테이너는 Tri Axle 섀시로 운송해야 함.

-- ISO Tank 컨테이너는 20ST가 일반적임
-- Flat Rack 컨테이너는 20ST, 40ST가 일반적임

-- Container 데이터 삽입
INSERT INTO Container (Container_ID, Status, Chassis_ID, Type, Size, Zone_ID)
SELECT 
    CONCAT('CT_', LPAD(t.num, 4, '0')) AS Container_ID,
    CASE WHEN t.num % 2 = 0 THEN 'Available' ELSE 'In Use' END AS Status,
    CONCAT('C_', LPAD(t.num, 4, '0')) AS Chassis_ID,
    CASE 
        WHEN t.num % 4 = 0 THEN 'Dry'
        WHEN t.num % 4 = 1 THEN 'Reefer'
        WHEN t.num % 4 = 2 THEN 'Flat Rack'
        ELSE 'ISO Tank'
    END AS Type,
    CASE 
        WHEN t.num % 3 = 0 THEN '40ST'
        WHEN t.num % 3 = 1 THEN '20ST'
        ELSE '45HC'
    END AS Size,
    CONCAT('CT_ZONE_', LPAD(t.num, 4, '0')) AS Zone_ID
FROM (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6
    UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12
    UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 UNION SELECT 16 UNION SELECT 17 UNION SELECT 18
    UNION SELECT 19 UNION SELECT 20 UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION SELECT 24
    UNION SELECT 25 UNION SELECT 26 UNION SELECT 27 UNION SELECT 28 UNION SELECT 29 UNION SELECT 30
) t;

-- 45' 컨테이너는 40피트 컨테이너 + 섀시와 동급임
-- 53' 컨테이너는 45피트 컨테이너 + 섀시와 동급임

-- Trailer 데이터 삽입
INSERT INTO Trailer (Trailer_ID, Status, Type, Zone_ID, Truck_ID)
SELECT 
    CONCAT('TL_', LPAD(t.num, 4, '0')) AS Trailer_ID,
    CASE WHEN t.num % 2 = 0 THEN 'Available' ELSE 'In Use' END AS Status,
    CASE WHEN t.num % 2 = 0 THEN '48\'' ELSE '53\'' END AS Type,
    CONCAT('TL_ZONE_', LPAD(t.num, 4, '0')) AS Zone_ID,
    CONCAT('T_', LPAD(t.num, 4, '0')) AS Truck_ID
FROM (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6
    UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12
    UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 UNION SELECT 16 UNION SELECT 17 UNION SELECT 18
    UNION SELECT 19 UNION SELECT 20 UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION SELECT 24
    UNION SELECT 25 UNION SELECT 26 UNION SELECT 27 UNION SELECT 28 UNION SELECT 29 UNION SELECT 30
) t;

-- Driver 데이터 삽입
INSERT INTO Driver (User_ID, Current_Location, Current_Status, Private_Truck_Info, Truck_ID)
SELECT 
    CONCAT('driver', LPAD(t.num, 3, '0')) AS User_ID,
    CASE 
        WHEN t.num % 5 = 1 THEN 'LA'
        WHEN t.num % 5 = 2 THEN 'PHX'
        WHEN t.num % 5 = 3 THEN 'HOU'
        WHEN t.num % 5 = 4 THEN 'SAV'
        ELSE 'MOB'
    END AS Current_Location,
    CASE WHEN t.num % 2 = 0 THEN 'In Use' ELSE 'Available' END AS Current_Status,
    CASE WHEN t.num % 3 = 0 THEN 'yes' ELSE 'no' END AS Private_Truck_Info,
    CONCAT('T_', LPAD(t.num, 4, '0')) AS Truck_ID
FROM (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6
) t;

-- Manager 테이블에 데이터 삽입
INSERT INTO Manager (User_ID, Position, Office_Phone, Division_ID)
SELECT 
    CONCAT('manager', LPAD(t.num, 3, '0')) AS User_ID,
    CASE 
        WHEN t.num = 1 THEN 'Senior Manager'
        WHEN t.num = 2 THEN 'Junior Manager'
        ELSE 'Assistant Manager'
    END AS Position,
    CONCAT('123-456-78', LPAD(t.num, 2, '0')) AS Office_Phone,
    CASE 
        WHEN t.num = 1 THEN 'LA'
        WHEN t.num = 2 THEN 'PHX'
        WHEN t.num = 3 THEN 'HOU'
        WHEN t.num = 4 THEN 'SAV'
        ELSE 'MOB'
    END AS Division_ID
FROM (
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
) t;

-- Password 데이터 삽입
INSERT INTO Password (User_ID, Password)
SELECT 
    User_ID, User_ID -- User_ID를 그대로 Password로 사용
FROM User;




-- Transport_Log 데이터 삽입
INSERT INTO Transport_Log (
    Driver_ID, Container_ID, Chassis_ID, Truck_ID, Trailer_ID, 
    Depart_Zone_ID, Depart_Date, Arrive_Zone_ID, Arrive_Date, Assigned, Log_Memo
)
SELECT 
    CONCAT('driver', LPAD(MOD(t.num - 1, 6) + 1, 3, '0')) AS Driver_ID, -- Driver_ID 순환
    CASE 
        WHEN MOD(t.num, 4) = 1 OR MOD(t.num, 4) = 2 THEN CONCAT('CT_', LPAD(t.num, 4, '0')) -- Container가 있는 경우
        ELSE NULL -- Trailer가 있는 경우 NULL
    END AS Container_ID,
    CASE 
        WHEN MOD(t.num, 4) = 2 THEN CONCAT('C_', LPAD(t.num, 4, '0')) -- Chassis는 Container와 함께 사용
        ELSE NULL -- 나머지 경우 NULL
    END AS Chassis_ID,
    CONCAT('T_', LPAD(MOD(t.num - 1, 6) + 1, 4, '0')) AS Truck_ID, -- Truck_ID는 항상 존재
    CASE 
        WHEN MOD(t.num, 4) = 0 THEN CONCAT('TL_', LPAD(t.num, 4, '0')) -- Trailer가 있는 경우
        ELSE NULL -- Trailer가 없는 경우 NULL
    END AS Trailer_ID,
    CONCAT('C_ZONE_', LPAD(t.num, 4, '0')) AS Depart_Zone_ID, -- 출발 Zone
    DATE_ADD(CURDATE(), INTERVAL t.num DAY) AS Depart_Date, -- 출발 날짜
    CONCAT('T_ZONE_', LPAD(t.num, 4, '0')) AS Arrive_Zone_ID, -- 도착 Zone
    DATE_ADD(CURDATE(), INTERVAL t.num + 1 DAY) AS Arrive_Date, -- 도착 날짜
    CASE
        WHEN MOD(t.num, 2) = 0 THEN TRUE -- 짝수일 경우 Assigned = TRUE
        ELSE FALSE -- 홀수일 경우 Assigned = FALSE
    END AS Assigned,
    CONCAT('Transport log entry #', t.num) AS Log_Memo -- 로그 메모
FROM (
    -- 숫자 1부터 20까지 생성
    SELECT 1 AS num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6
    UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12
    UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 UNION SELECT 16 UNION SELECT 17 UNION SELECT 18
    UNION SELECT 19 UNION SELECT 20
) t
WHERE CONCAT('T_', LPAD(MOD(t.num - 1, 6) + 1, 4, '0')) IN (
    SELECT Truck_ID FROM Truck -- Truck 테이블의 Truck_ID를 참조
);
