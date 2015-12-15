from datamodel import *
from sqlalchemy import create_engine, or_ , and_
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine ('sqlite:///studentips_db.sqlite')
Session = scoped_session (sessionmaker (bind=engine))

Base .metadata.create_all(engine)
Base.query = Session.query_property()

session = Session()

def add_tip():
    return True

#search professor by name (or search parameter)
def search_professor(prof):
    professors = Professor.query.all()
    for professor in professors:
        if(str(prof).lower() in str(professor.first_name + " " + professor.last_name).lower()) or (str(prof).lower() in str(professor.last_name + " " + professor.first_name).lower()):
            return professor.id
    return False

#search prof_course
def search_profcourse_tips(course, prof):
    id_prof = search_professor(prof)
    if(id_prof == False):
        return False
    else:
        courses_prof = Prof_Course.query.filter(Prof_Course.prof_id == id_prof)
        for prof_course in courses_prof:
            if str((prof_course.course_name)).lower() == str(course).lower():
                id_profcourse = prof_course.id
                tips = Tip.query.filter(Tip.prof_course == id_profcourse)
                return tips
        return False

def search_university(name):
    universities = University.query.all()
    for university in universities:
        if(str(name).lower() in str(university.name).lower()):
            return university
    return False

#get info about the user
def get_user(email):
    users = User.query.filter(User.email == email)
    for user in users:
        return user
    return False

#check if user exists
def check_user(email, password):
    users = User.query.filter(and_(User.email == email, User.password == password))
    for user in users:
        #it means that we have actually one user with these credentials
        return user
    return False

#insert new user
def insert_user(email, password, first_name, last_name, university, faculty, phone_number):
    if not (get_user(email) == False):
        return False
    else:
        newUser = User(email, password, first_name, last_name, university, faculty, phone_number, 'ENG')
        session.add(newUser)
        session.commit()
        session.flush()
        return get_user(email)

#undo changes on the database
def undo_changes():
    session.rollback()