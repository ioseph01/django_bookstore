## About
A online bookstore project.

## Tech Stack
- **Backend**: Python, Django 5.2
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: PostgreSQL with psycopg2
- **Deployment**: AWS EC2, AWS RDS, Gunicorn
- **Environment Management**: python-dotenv, uv

## AWS Deployment
### EC2 Setup
- Instance type: t3.micro
- Security groups: Allow port 8000, SSH

### RDS Setup  
- Engine: PostgreSQL
- Connection details in .env

### Django Configuration
- Set ALLOWED_HOSTS in .env
- Run: `uv run gunicorn myproject.wsgi:application --bind 0.0.0.0:8000`
- Use screen session for persistence

## For Local Development
1. Clone the repo
2. Install dependencies: `uv sync`
3. Setup local database and users:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE db_name;
   CREATE USER user_name WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE db_name TO user_name;
   \q
4. Complete .env variables
5. Populate local database: `uv run manage.py import_books books.json`
6. Run migrations: `uv run manage.py migrate`
7. Start server: `uv run manage.py runserver`

## Environment Variables
- DB_NAME=your_database_name
- DB_USER=your_username
- DB_PASSWORD=your_password_here
- DB_HOST=localhost
- DB_PORT=5432
- SECRET_KEY=your_secret_key_here
- DEBUG=True