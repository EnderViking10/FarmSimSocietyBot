import os
from datetime import datetime

from discord import Member
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Base class for models
Base = declarative_base()

# Database connection string
db_user = os.getenv("db_username")
db_password = os.getenv("db_password")
db_name = os.getenv("db_name")
ENV = os.getenv("ENV", "development")
DATABASE_URL = os.getenv(
    "DATABASE_URL_DEV",
    "sqlite:///data/dev.db",
) if ENV == "development" else os.getenv(
    "DATABASE_URL_PROD",
    f"mysql+pymysql://{db_user}:{db_password}@localhost/{db_name}",
)

# Initialize the database engine
engine = create_engine(DATABASE_URL, echo=False)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Example model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    discord_id = Column(Integer, nullable=False, index=True, unique=True)
    join_date = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def get_user(cls, db, discord_id: int):
        return db.query(cls).filter_by(discord_id=discord_id).first()

    @classmethod
    def update_username(cls, db, discord_id: int, username: str):
        user = db.query(cls).filter_by(discord_id=discord_id).first()
        user.username = username
        db.commit()

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, discord_id={self.discord_id})>"


class Bank(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(Integer, ForeignKey("users.discord_id"), nullable=False, unique=True)
    balance = Column(Integer, nullable=False, default=10000)

    @classmethod
    def get_bank(cls, db, discord_id: int):
        return db.query(cls).filter_by(discord_id=discord_id).first()

    def __repr__(self):
        return f"<Bank(id={self.id}, discord_id={self.discord_id}, balance={self.balance})>"


# Initialize database
def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


# Dependency for accessing database sessions
def get_db():
    """Yield a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Adds user to the database
def add_user(member: Member):
    from bot import logger
    db = next(get_db())
    new_user = User(username=member.name, discord_id=member.id)
    new_bank = Bank(discord_id=member.id)
    db.add(new_user)
    db.add(new_bank)
    db.commit()
    db.close()
    logger.info(f"{member.name} : {member.id} added to the database")
