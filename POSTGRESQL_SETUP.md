# Установка и настройка PostgreSQL

## Для Windows:
1. Скачайте PostgreSQL с https://www.postgresql.org/download/windows/
2. Установите с настройками по умолчанию
3. Запомните пароль для пользователя postgres
4. Запустите pgAdmin или используйте командную строку

## Для Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Создание базы данных и пользователя:
sudo -u postgres psql
CREATE DATABASE lms_platform;
CREATE USER lms_user WITH PASSWORD 'password';
ALTER ROLE lms_user SET client_encoding TO 'utf8';
ALTER ROLE lms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE lms_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE lms_platform TO lms_user;
\q
