-- Olfit RDB 데이터베이스 초기화
CREATE DATABASE IF NOT EXISTS olfit_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE DATABASE IF NOT EXISTS test_olfit_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- Olfit 전용 사용자 생성 및 권한 부여
-- .env의 SQL_DB_USER, SQL_DB_PASSWORD와 일치시켜야 함
CREATE USER IF NOT EXISTS 'olfit_admin'@'%' IDENTIFIED WITH mysql_native_password BY 'olfit_password';

GRANT ALL PRIVILEGES ON olfit_db.* TO 'olfit_admin'@'%';
GRANT ALL PRIVILEGES ON test_olfit_db.* TO 'olfit_admin'@'%';

FLUSH PRIVILEGES;
