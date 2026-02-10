import pytest
import time
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

Base = declarative_base()
DATABASE_URL = "postgresql://анастасия:popa666@localhost:5432/postgres"

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

def generate_unique_name(base_name):
    return f"{base_name} {int(time.time() * 1000)}"

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
        session.query(Subject).filter(Subject.name.like('Test Subject%')).delete()
        session.query(Subject).filter(Subject.name.like('Updated Subject%')).delete()
        session.query(Subject).filter(Subject.name.like('New Test Subject%')).delete()
        session.query(Subject).filter(Subject.name.like('Unique Test Subject%')).delete()
        session.commit()
        session.close()

def test_create_subject(db_session):
    subject_name = generate_unique_name("New Test Subject")
    new_subject = Subject(name=subject_name)
    db_session.add(new_subject)
    db_session.commit()
    db_session.refresh(new_subject)
    
    subject_from_db = db_session.query(Subject).filter(
        Subject.name == subject_name
    ).first()
    
    assert subject_from_db is not None
    assert subject_from_db.name == subject_name
    assert subject_from_db.id is not None

def test_update_subject(db_session):
    original_name = generate_unique_name("Test Subject")
    subject = Subject(name=original_name)
    db_session.add(subject)
    db_session.commit()
    db_session.refresh(subject)
    
    updated_name = generate_unique_name("Updated Subject")
    subject_to_update = db_session.query(Subject).get(subject.id)
    subject_to_update.name = updated_name
    db_session.commit()
    
    updated_subject = db_session.query(Subject).get(subject.id)
    assert updated_subject.name == updated_name
    assert updated_subject.name != original_name

def test_delete_subject(db_session):
    subject_name = generate_unique_name("Test Subject")
    subject = Subject(name=subject_name)
    db_session.add(subject)
    db_session.commit()
    db_session.refresh(subject)
    
    subject_before_delete = db_session.query(Subject).get(subject.id)
    assert subject_before_delete is not None
    
    subject_to_delete = db_session.query(Subject).get(subject.id)
    db_session.delete(subject_to_delete)
    db_session.commit()
    
    subject_after_delete = db_session.query(Subject).get(subject.id)
    assert subject_after_delete is None

def test_subject_unique_constraint(db_session):
    subject_name = generate_unique_name("Unique Test Subject")
    subject1 = Subject(name=subject_name)
    db_session.add(subject1)
    db_session.commit()
    
    subject2 = Subject(name=subject_name)
    db_session.add(subject2)
    
    with pytest.raises(IntegrityError):
        db_session.commit()
    
    db_session.rollback()
