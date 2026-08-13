# DB Configuration

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.database.app.config import settings

engine = create_engine(
    settings.database_url,
    echo=True,
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
)

