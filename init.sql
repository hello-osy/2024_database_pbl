-- YMS_db 데이터베이스 생성 및 선택
CREATE DATABASE IF NOT EXISTS `YMS_db`;
USE `YMS_db`;

-- 사용자에게 권한 부여
GRANT ALL PRIVILEGES ON YMS_db.* TO 'user'@'%';

-- 변경 사항 적용
FLUSH PRIVILEGES;

-- Address 테이블 생성
CREATE TABLE `Address` (
    `Address_ID` INT NOT NULL AUTO_INCREMENT,
    `House_Number` VARCHAR(20) NULL,
    `Street_Name` VARCHAR(20) NULL,
    `City` VARCHAR(20) NULL,
    `ZipCode` INT NULL,
    PRIMARY KEY (`Address_ID`)
);

-- Division 테이블 생성
CREATE TABLE `Division` (
    `Division_ID` VARCHAR(10) NOT NULL,
    `Division_Name` VARCHAR(30) NOT NULL,
    `Address_ID` INT NOT NULL,
    PRIMARY KEY (`Division_ID`),
    FOREIGN KEY (`Address_ID`) REFERENCES `Address`(`Address_ID`)
);

-- Yard 테이블 생성
CREATE TABLE `Yard` (
    `Yard_ID` VARCHAR(20) NOT NULL,
    `Division_ID` VARCHAR(10) NOT NULL,
    `Yard_Name` VARCHAR(30) NOT NULL,
    `Site_ID` VARCHAR(20) NULL,
    `Address_ID` INT NOT NULL,
    PRIMARY KEY (`Yard_ID`),
    FOREIGN KEY (`Division_ID`) REFERENCES `Division`(`Division_ID`),
    FOREIGN KEY (`Address_ID`) REFERENCES `Address`(`Address_ID`)
);

-- Site 테이블 생성
CREATE TABLE `Site` (
    `Site_ID` VARCHAR(20) NOT NULL,
    `Yard_ID` VARCHAR(20) NOT NULL,
    `Site_Name` VARCHAR(30) NULL,
    `Address_ID` INT NOT NULL,
    `y_Cordinate` INT NULL,
    `x_Cordinate` INT NULL,
    `y_Max_Size` INT NULL,
    `x_Max_Size` INT NULL,
    PRIMARY KEY (`Site_ID`),
    FOREIGN KEY (`Yard_ID`) REFERENCES `Yard`(`Yard_ID`),
    FOREIGN KEY (`Address_ID`) REFERENCES `Address`(`Address_ID`)
);

-- Zone 테이블 생성
CREATE TABLE `Zone` (
    `Zone_ID` VARCHAR(30) NOT NULL,
    `Site_ID` VARCHAR(20) NOT NULL,
    `Status` VARCHAR(20) NULL,
    `Storage_Type` VARCHAR(20) NULL,
    `y_Cordinate` INT NULL,
    `x_Cordinate` INT NULL,
    PRIMARY KEY (`Zone_ID`),
    FOREIGN KEY (`Site_ID`) REFERENCES `Site`(`Site_ID`)
);

-- Truck 테이블 생성
CREATE TABLE `Truck` (
    `Truck_ID` VARCHAR(10) NOT NULL,
    `Status` VARCHAR(20) NULL,
    `Zone_ID` VARCHAR(30) NOT NULL,
    PRIMARY KEY (`Truck_ID`),
    FOREIGN KEY (`Zone_ID`) REFERENCES `Zone`(`Zone_ID`)
);

-- Chassis 테이블 생성
CREATE TABLE `Chassis` (
    `Chassis_ID` VARCHAR(10) NOT NULL,
    `Status` VARCHAR(20) NULL,
    `Type` VARCHAR(20) NULL,
    `Truck_ID` VARCHAR(10) NOT NULL,
    `Zone_ID` VARCHAR(30) NOT NULL,
    PRIMARY KEY (`Chassis_ID`),
    FOREIGN KEY (`Truck_ID`) REFERENCES `Truck`(`Truck_ID`),
    FOREIGN KEY (`Zone_ID`) REFERENCES `Zone`(`Zone_ID`)
);

-- Container 테이블 생성
CREATE TABLE `Container` (
    `Container_ID` VARCHAR(20) NOT NULL,
    `Status` VARCHAR(20) NULL,
    `Chassis_ID` VARCHAR(10) NOT NULL,
    `Type` VARCHAR(255) NULL,
    `Zone_ID` VARCHAR(30) NOT NULL,
    PRIMARY KEY (`Container_ID`),
    FOREIGN KEY (`Chassis_ID`) REFERENCES `Chassis`(`Chassis_ID`),
    FOREIGN KEY (`Zone_ID`) REFERENCES `Zone`(`Zone_ID`)
);

-- Trailer 테이블 생성
CREATE TABLE `Trailer` (
    `Trailer_ID` VARCHAR(10) NOT NULL,
    `Status` VARCHAR(20) NULL,
    `Type` VARCHAR(20) NULL,
    `Zone_ID` VARCHAR(30) NOT NULL,
    `Truck_ID` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`Trailer_ID`),
    FOREIGN KEY (`Zone_ID`) REFERENCES `Zone`(`Zone_ID`),
    FOREIGN KEY (`Truck_ID`) REFERENCES `Truck`(`Truck_ID`)
);

-- User 테이블 생성
CREATE TABLE `User` (
    `User_ID` VARCHAR(20) NOT NULL,
    `UserName` VARCHAR(50) NOT NULL,
    `Email` VARCHAR(100) NULL,
    `Role_ID` INT NULL,
    `Phone_Number` VARCHAR(20) NULL,
    PRIMARY KEY (`User_ID`)
);

-- Driver 테이블 생성
CREATE TABLE `Driver` (
    `User_ID` VARCHAR(20) NOT NULL,
    `Current_Location` INT NOT NULL,
    `Current_Status` VARCHAR(20) NULL,
    `Private_Truck_Info` VARCHAR(20) NULL,
    `Truck_ID` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`User_ID`),
    FOREIGN KEY (`User_ID`) REFERENCES `User`(`User_ID`),
    FOREIGN KEY (`Truck_ID`) REFERENCES `Truck`(`Truck_ID`)
);

-- Manager 테이블 생성
CREATE TABLE `Manager` (
    `User_ID` VARCHAR(20) NOT NULL,
    `Position` VARCHAR(50) NULL,
    `Office_Phone` VARCHAR(20) NULL,
    `Division_ID` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`User_ID`),
    FOREIGN KEY (`User_ID`) REFERENCES `User`(`User_ID`),
    FOREIGN KEY (`Division_ID`) REFERENCES `Division`(`Division_ID`)
);

-- Password 테이블 생성
CREATE TABLE `Password` (
    `User_ID` VARCHAR(20) NOT NULL,
    `Password` VARCHAR(255) NULL,
    PRIMARY KEY (`User_ID`),
    FOREIGN KEY (`User_ID`) REFERENCES `User`(`User_ID`)
);

-- Tranport_Log 테이블 생성
CREATE TABLE `Tranport_Log` (
    `Log_ID` INT NOT NULL AUTO_INCREMENT,
    `Driver_ID` VARCHAR(20) NOT NULL,
    `Container_ID` VARCHAR(20) NOT NULL,
    `Chassis_ID` VARCHAR(10) NOT NULL,
    `Truck_ID` VARCHAR(10) NOT NULL,
    `Trailer_ID` VARCHAR(10) NOT NULL,
    `Depart_Zone_ID` VARCHAR(30) NOT NULL,
    `Depart_Date` DATE NULL,
    `Arrive_Zone_ID` VARCHAR(30) NOT NULL,
    `Arrive_Date` DATE NULL,
    `Log_Memo` VARCHAR(30) NULL,
    PRIMARY KEY (`Log_ID`),
    FOREIGN KEY (`Driver_ID`) REFERENCES `Driver`(`User_ID`),
    FOREIGN KEY (`Container_ID`) REFERENCES `Container`(`Container_ID`),
    FOREIGN KEY (`Chassis_ID`) REFERENCES `Chassis`(`Chassis_ID`),
    FOREIGN KEY (`Truck_ID`) REFERENCES `Truck`(`Truck_ID`),
    FOREIGN KEY (`Trailer_ID`) REFERENCES `Trailer`(`Trailer_ID`),
    FOREIGN KEY (`Depart_Zone_ID`) REFERENCES `Zone`(`Zone_ID`),
    FOREIGN KEY (`Arrive_Zone_ID`) REFERENCES `Zone`(`Zone_ID`)
);

-- 테스트 데이터 삽입

-- Address 데이터 삽입
INSERT INTO `Address` (`House_Number`, `Street_Name`, `City`, `ZipCode`) VALUES
    ('100', 'Main St', 'Los Angeles', 90001),
    ('200', '2nd Ave', 'Phoenix', 85001),
    ('300', '3rd Blvd', 'Houston', 77001),
    ('400', '4th St', 'Savannah', 31401),
    ('500', '5th Ave', 'Mobile', 36601);

-- Division 데이터 삽입
INSERT INTO `Division` (`Division_ID`, `Division_Name`, `Address_ID`) VALUES
    ('LA', 'Los Angeles', 1),
    ('PHX', 'Phoenix', 2),
    ('HOU', 'Houston', 3),
    ('SAV', 'Savannah', 4),
    ('MOB', 'Mobile', 5);

-- Yard 데이터 삽입
INSERT INTO `Yard` (`Yard_ID`, `Division_ID`, `Yard_Name`, `Site_ID`, `Address_ID`) VALUES
    ('HOU_YARD_01', 'HOU', 'Yard 1 HOU', 'HOU_SITE_01', 3),
    ('LA_YARD_01', 'LA', 'Yard 1 LA', 'LA_SITE_01', 1),
    ('MOB_YARD_01', 'MOB', 'Yard 1 MOB', 'MOB_SITE_01', 5),
    ('PHX_YARD_01', 'PHX', 'Yard 1 PHX', 'PHX_SITE_01', 2),
    ('SAV_YARD_01', 'SAV', 'Yard 1 SAV', 'SAV_SITE_01', 4);

-- Site 데이터 삽입
INSERT INTO `Site` (`Site_ID`, `Yard_ID`, `Site_Name`, `Address_ID`, `y_Cordinate`, `x_Cordinate`, `y_Max_Size`, `x_Max_Size`) VALUES
    ('HOU_SITE_01', 'HOU_YARD_01', 'Site 1 HOU', 3, 2, 2, 100, 100),
    ('LA_SITE_01', 'LA_YARD_01', 'Site 1 LA', 1, 0, 0, 100, 100),
    ('MOB_SITE_01', 'MOB_YARD_01', 'Site 1 MOB', 5, 4, 4, 100, 100),
    ('PHX_SITE_01', 'PHX_YARD_01', 'Site 1 PHX', 2, 1, 1, 100, 100),
    ('SAV_SITE_01', 'SAV_YARD_01', 'Site 1 SAV', 4, 3, 3, 100, 100);

-- Zone 데이터 삽입
INSERT INTO `Zone` (`Zone_ID`, `Site_ID`, `Status`, `Storage_Type`, `y_Cordinate`, `x_Cordinate`) VALUES
    ('CHASSIS_ZONE_01', 'LA_SITE_01', 'In Use', 'Chassis', 0, 0),
    ('CHASSIS_ZONE_02', 'PHX_SITE_01', 'Available', 'Chassis', 1, 1),
    ('CHASSIS_ZONE_03', 'HOU_SITE_01', 'In Use', 'Chassis', 2, 2),
    ('CHASSIS_ZONE_04', 'SAV_SITE_01', 'Available', 'Chassis', 3, 3),
    ('CONTAINER_ZONE_01', 'LA_SITE_01', 'Loaded', 'Container', 0, 0),
    ('CONTAINER_ZONE_02', 'PHX_SITE_01', 'Empty', 'Container', 1, 1),
    ('TRAILER_ZONE_01', 'LA_SITE_01', 'In Use', 'Trailer', 0, 0),
    ('TRAILER_ZONE_02', 'PHX_SITE_01', 'Available', 'Trailer', 1, 1),
    ('TRUCK_ZONE_01', 'LA_SITE_01', 'Available', 'Truck', 0, 0),
    ('TRUCK_ZONE_02', 'PHX_SITE_01', 'Available', 'Truck', 1, 1),
    ('TRUCK_ZONE_03', 'HOU_SITE_01', 'Available', 'Truck', 2, 2),
    ('TRUCK_ZONE_04', 'SAV_SITE_01', 'Available', 'Truck', 3, 3);

-- Truck 데이터 삽입
INSERT INTO `Truck` (`Truck_ID`, `Status`, `Zone_ID`) VALUES
    ('TRK1', 'Active', 'TRUCK_ZONE_01'),
    ('TRK2', 'Available', 'TRUCK_ZONE_02'),
    ('TRK3', 'Active', 'TRUCK_ZONE_03'),
    ('TRK4', 'Available', 'TRUCK_ZONE_04');

-- Chassis 데이터 삽입
INSERT INTO `Chassis` (`Chassis_ID`, `Status`, `Type`, `Truck_ID`, `Zone_ID`) VALUES
    ('CHAS1', 'In Use', 'Regular', 'TRK1', 'CHASSIS_ZONE_01'),
    ('CHAS2', 'Available', 'Light', 'TRK2', 'CHASSIS_ZONE_02'),
    ('CHAS3', 'In Use', 'Tandem', 'TRK3', 'CHASSIS_ZONE_03'),
    ('CHAS4', 'Available', 'Tri Axle', 'TRK4', 'CHASSIS_ZONE_04');

-- Container 데이터 삽입
INSERT INTO `Container` (`Container_ID`, `Status`, `Chassis_ID`, `Type`, `Zone_ID`) VALUES
    ('CONT00001', 'Loaded', 'CHAS1', 'Dry', 'CONTAINER_ZONE_01'),
    ('CONT00002', 'Empty', 'CHAS2', 'Reefer', 'CONTAINER_ZONE_02');

-- Trailer 데이터 삽입
INSERT INTO `Trailer` (`Trailer_ID`, `Status`, `Type`, `Zone_ID`, `Truck_ID`) VALUES
    ('TRLR000001', 'In Use', '53\'', 'TRAILER_ZONE_01', 'TRK1'),
    ('TRLR000002', 'Available', '48\'', 'TRAILER_ZONE_02', 'TRK2');

-- User 데이터 삽입
INSERT INTO `User` (`User_ID`, `UserName`, `Email`, `Role_ID`, `Phone_Number`) VALUES
    ('driver001', 'Driver 1', 'driver1@example.com', 2, '123-456-7890'),
    ('driver002', 'Driver 2', 'driver2@example.com', 2, '123-456-7891'),
    ('manager001', 'Manager 1', 'manager1@example.com', 1, '123-456-7892'),
    ('manager002', 'Manager 2', 'manager2@example.com', 1, '123-456-7893');

-- Driver 데이터 삽입
INSERT INTO `Driver` (`User_ID`, `Current_Location`, `Current_Status`, `Private_Truck_Info`, `Truck_ID`) VALUES
    ('driver001', 1, 'Active', 'Private Info', 'TRK1');

-- Manager 데이터 삽입
INSERT INTO `Manager` (`User_ID`, `Position`, `Office_Phone`, `Division_ID`) VALUES
    ('manager001', 'Senior Manager', '123-456-7892', 'LA'),
    ('manager002', 'Junior Manager', '123-456-7893', 'PHX');

-- Password 데이터 삽입
INSERT INTO `Password` (`User_ID`, `Password`) VALUES
    ('driver001', 'driver001'),
    ('driver002', 'driver002'),
    ('manager001', 'manager001'),
    ('manager002', 'manager002');
