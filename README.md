# python_fastapi

1. Create a .venv and activate:  
`python -m venv .venv && source .venv/bin/activate`
2. Check if your databases are well configured.
3initialize fastapi:  
`uvicorn {app_xxx}.main:app --reload` *[change {app_xxx} for app_psycopg or app_sqlalchemy]*
3. Done!