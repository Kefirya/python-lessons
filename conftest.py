import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Subject

DATABASE_URL = "postgresql://postgres:aA123123@localhost:5432/postgres"

@pytest.fixture(scope="session")
def engine():
    return create_engine(DATABASE_URL)

@pytest.fixture
def db_session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        yield session
    finally:
        # Cleanup test data
        session.query(Subject).filter(
            Subject.name.like('Test Subject%') |
            Subject.name.like('Updated Subject%') |
            Subject.name.like('New Test Subject%') |
            Subject.name.like('Unique Test Subject%')
        ).delete(synchronize_session=False)
        session.commit()
        session.close()
