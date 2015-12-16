from datamodel import *
from sqlalchemy import create_engine, or_ , and_
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine ('sqlite:///studentips_db.sqlite')

Session = scoped_session (sessionmaker (bind=engine))

Base .metadata.create_all(engine)
Base.query = Session.query_property()

session = Session()

"""Universities"""
session.add_all([
    University('Politecnico di Torino'),
    University('Politecnico di Milano'),
    University('Politecnico di Bari')
])
session.commit()

"""Courses"""
session.add_all([
    Course('Economics'),
    Course('Information Systems'),
    Course('Accounting and Corporate Finance'),
    Course('Analysis and Management of Production Systems'),
    Course('Business law'),
    Course('Industrial Economics'),
    Course('Strategy and Organization')
])

session.commit()

"""Language"""
session.add_all([
    Language (id='ENG', name='english')
])

session.commit()

"""Professors"""
session.add_all([
    Professor('Elisa', 'Ughetto'),
    Professor('Claudio', 'Demartini'),
    Professor('Agostino', 'Villa'),
    Professor('Paolo', 'Rainelli'),
    Professor('Luca', 'Abate'),
    Professor('Luigi', 'Benfratello'),
    Professor('Paolo', 'Neirotti'),
])

session.commit()

"""Pro_Course association"""
session.add_all([
    Prof_Course(prof_id=5,course_name="Economics"),
    Prof_Course(prof_id=6,course_name="Economics"),
    Prof_Course(prof_id=2,course_name="Information Systems"),
    Prof_Course(prof_id=1,course_name="Accounting and Corporate Finance"),
    Prof_Course(prof_id=4,course_name="Analysis and Management of Production Systems"),
    Prof_Course(prof_id=3,course_name="Business law"),
    Prof_Course(prof_id=6,course_name="Industrial Economics"),
    Prof_Course(prof_id=7,course_name="Strategy and Organization")
])

session.commit()

"""Users"""
session.add_all([
    User('john.lennon@gmail.com', 'beatles', 'John', 'Lennon', 'Politecnico di Torino', 'Engineering and Management', '3203293333', 'ENG'),
    User('paul.mccartney@gmail.com','beatles', 'Paul', 'McCartney', 'Politecnico di Torino', 'Engineering and Management', '3203291111', 'ENG'),
    User('george.harrison@gmail.com', 'beatles', 'George', 'Harrison', 'Politecnico di Torino', 'Engineering and Management', '3203292222', 'ENG'),
    User('ringo.starr@gmail.com', 'beatles', 'Ringo', 'Starr', 'Politecnico di Torino', 'Engineering and Management', '3203294444', 'ENG'),
])

session.commit()

"""Tips"""
session.add_all([
    Tip('john.lennon@gmail.com', 1, 4, 2, 5, 1, 4, 2, 4, 5, 3, 2, 'Slides are the way.'),
    Tip('paul.mccartney@gmail.com', 1, 5, 5, 5, 3, 3, 3, 4, 5, 4, 3, 'Ask the professor if you have problems.'),
    Tip('george.harrison@gmail.com', 1, 1, 1, 3, 2, 3, 2, 4, 5, 1, 3, 'This course will destroy your life.'),
    Tip('ringo.starr@gmail.com', 1, 4, 4, 4, 3, 5, 1, 3, 1, 3, 3, 'Easy. Cool.')
])

session.commit()

