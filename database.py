import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, select, DateTime, Integer, Boolean, Text, and_
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# DATABASE_URL = "sqlite:///database.sqlite3"
DATABASE_URL = "postgresql://postgres:JuXzDuUXGqPHVNcrgdQVZIDZhTefejRC@tramway.proxy.rlwy.net:54646/railway"
# DATABASE_URL = "postgresql://smart_food_user:IAb8lvnJBTGbiJBpol4Yti6k5yhRuC2o@dpg-cu8i7t8gph6c73cpshe0-a.oregon-postgres.render.com/smart_food"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class Questions_and_answers(Base):
    __tablename__ = "questions_and_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String, nullable=False)
    questions = Column(String, nullable=False)
    grade = Column(String, nullable=False)


class Candidates(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ FIXED
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    grade = Column(Integer, nullable=False)
    answers = Column(String, nullable=True,default="")
    subject_name = Column(String, nullable=False)
    score = Column(String, nullable=False, default=0)


def create_quests_and_answers(subject_name, questions, grade):
    with SessionLocal() as session:
        r = session.query(Questions_and_answers).filter_by(
            subject_name=subject_name,
            grade=grade
        ).first()
        if r:
            return r

        new_obj = Questions_and_answers(
            subject_name=subject_name,
            questions=questions,
            grade=grade,
        )
        session.add(new_obj)
        session.commit()
        return new_obj


def get_questions_and_answers(subject_name, grade):
    with SessionLocal() as session:
        r = session.query(Questions_and_answers).filter_by(
            subject_name=subject_name,
            grade=grade
        ).first()
        return r if r else False


def get_or_create_candidates(name, surname, grade, subject_name):
    with SessionLocal() as session:
        r = session.query(Candidates).filter_by(
            name=name, surname=surname, grade=grade, subject_name=subject_name
        ).first()
        if r:
            return {"id": r.id, "name": r.name, "surname": r.surname, "grade": r.grade, "subject": r.subject_name,'new_user':False}

        new_candidate = Candidates(name=name, surname=surname, grade=grade, subject_name=subject_name)
        session.add(new_candidate)
        session.commit()
        session.refresh(new_candidate)  # ensures id is available
        return {"id": new_candidate.id, "name": new_candidate.name, "surname": new_candidate.surname,
                "grade": new_candidate.grade, "subject": new_candidate.subject_name,'new_user':True}

def delete_candidate(candidate_id):
    with SessionLocal() as session:
        r = session.query(Candidates).filter_by(id=candidate_id).first()
        if r:
            session.delete(r)
            session.commit()
            return True
        return False

def update_candidate(id, score,answers=None):
    with SessionLocal() as session:
        r = session.query(Candidates).filter_by(id=id).first()
        if r:
            r.score = score
            if answers:
                r.answers = answers
            session.commit()
            return True
        return False


def all_users():
    with SessionLocal() as session:
        r = session.query(Candidates).all()
        if r:
            a = {}
            for i in r:
                a[i.id]={"name": i.name, "answers":i.answers,"surname": i.surname,"score":i.score,
                        "grade": i.grade, "subject": i.subject_name,'new_user':True}
            return a
        return False


def init():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)   # <- creates all missing tables

if __name__ == "__main__":
    init()
