# FarmSim Society

This is a discord bot used in the `FarmSim Society` FS community.

# Database Schema

- Users
    - id Integer Primary Key
    - username String
    - discord_id Integer
    - join_date (DATETIME DEFAULT DATETIME NOW)
- Bank
    - id INTEGER PRIMARY KEY
    - discord_id INTEGER FOREIGN KEY users(discord_id)
    - balance INTEGER default 10000
- Servers
  - id INTEGER PRIMARY KEY
  - ip String

# Alembic commands
```shell
# Create new database revision
alembic revision --autogenerate -m "Description"

# Migrate to new revision
alembic upgrade head

# View history
alembic history
```

# Requirements

- aiohappyeyeballs==2.4.3
- aiohttp==3.11.8
- aiosignal==1.3.1
- alembic==1.14.0
- async-timeout==5.0.1
- attrs==24.2.0
- certifi==2024.8.30
- charset-normalizer==3.4.0
- discord.py==2.4.0
- frozenlist==1.5.0
- greenlet==3.1.1
- idna==3.10
- Mako==1.3.6
- MarkupSafe==3.0.2
- multidict==6.1.0
- propcache==0.2.0
- PyMySQL==1.1.1
- python-dotenv==1.0.1
- requests==2.32.3
- SQLAlchemy==2.0.36
- typing_extensions==4.12.2
- urllib3==2.2.3
- yarl==1.18.0

# Todo

- Log every command run
    - To channel
- Transfer command
  - Integrate with mod using xml and shit??

