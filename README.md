# python_fastapi

### Postgres Container
If you don`t have Docker installed, install it, then run (inside the python_fastapi folder):
1. `docker pull postgres`
2. `docker run --name pgsql --rm -p 5432:5432 --env-file ./.env_postgres -d postgres`

### Application
1. Create a .venv and activate:  
`python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
2. Check if your databases are well configured.
3initialize fastapi:  
`uvicorn {app_xxx}.main:app --reload` *[change {app_xxx} for app_psycopg or app_sqlalchemy]*
3. Done!