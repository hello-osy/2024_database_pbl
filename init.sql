-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS my_database;

-- 사용자 생성 및 비밀번호 설정
CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'user_password';

-- 데이터베이스에 대한 권한 부여
GRANT ALL PRIVILEGES ON my_database.* TO 'user'@'%';

-- 권한 적용
FLUSH PRIVILEGES;

-- 데이터베이스 사용
USE my_database;

-- 테이블 생성
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 기본 데이터 삽입
INSERT INTO users (name, email, age) VALUES
('Alice', 'alice@example.com', 25),
('Bob', 'bob@example.com', 30),
('Charlie', 'charlie@example.com', 28);
