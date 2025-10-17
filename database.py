from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
import os

database_url = os.getenv('DATABASE_URL')
engine = create_async_engine(database_url, echo=True)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)

Base = declarative_base()

class PersonDB(Base):
    __tablename__ = "people"
    __table_args__ = (UniqueConstraint('first_name', name='unique_first_name'),)

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False, unique=True, index=True)
    last_name = Column(String(100), nullable=False)
    mother_id = Column(Integer, ForeignKey("people.id"), nullable=True)
    father_id = Column(Integer, ForeignKey("people.id"), nullable=True)

    mother = relationship("PersonDB", foreign_keys=[mother_id], remote_side=[id], backref="children_as_mother")
    father = relationship("PersonDB", foreign_keys=[father_id], remote_side=[id], backref="children_as_father")

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()