from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
import datetime

Base = declarative_base()

#forma classica
"""
class Padre(Base):

    __tablename__='padre'

    name=Column(String, primary_key=True)
    figli=relationship("Figlio")

class Figlio(Base):

    __tablename__= 'figlio'

    name=Column(String, primary_key=True)
    padre_name=Column(String, ForeignKey('padre.name'))
"""

#doppio backref
"""
class Padre(Base):

    __tablename__='padre'

    name=Column(String, primary_key=True)


class Figlio(Base):

    __tablename__= 'figlio'

    name=Column(String, primary_key=True)
    padre_name=Column(String, ForeignKey('padre.name'))
    padre = relationship("Padre", backref= backref('figli',uselist=True,cascade='delete,all'))
"""

def current_time():
    time = str(datetime.datetime.now())
    return str(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f').strftime('%d-%m-%y %H:%M'))


class Course(Base):

    __tablename__ = 'course'

    name = Column(String, primary_key=True)
    description = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
         return "<Course('%s')>" % (self.name)


class Language(Base):

    __tablename__ = 'language'

    id = Column(String, primary_key=True)
    name = Column(String)
    file = Column(String)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
         return "<Language('%s', '%s')>" % (self.id, self.name)


class University(Base):

    __tablename__ = 'university'

    name = Column(String, primary_key=True)
    num_tips = Column(Integer)
    _quality = Column(Float)
    _availability = Column(Float)
    _participation = Column(Float)
    _difficulty = Column(Float)

    def __init__(self, name):
        self.name = name
        self.num_tips=0
        self._quality=0
        self._availability=0
        self._difficulty=0
        self._participation=0

    def __repr__(self):
        return "<University ( '%s' , '%d' , '%f' , '%f' , '%f' , '%f' )>" % (self.name, self.num_tips, self._quality, self._availability, self._difficulty, self._participation)

    def update_rating (self, tip):
        self._quality = (self._quality * self.num_tips + tip['_teaching'])/(self.num_tips+1)
        self._availability = (self._availability * self.num_tips + tip['_availability'])/(self.num_tips+1)
        self._participation = (self._participation * self.num_tips + tip['_participation'])/(self.num_tips+1)
        self._difficulty = (self._quality * self.num_tips + tip['_difficulty'])/(self.num_tips+1)
        self.num_tips+=1
    def get_info (self):

        info = {}
        info['name']=self.name
        info['_quality']=self._quality
        info['_availability'] = self._availability
        info['_difficulty'] = self._difficulty
        info['_participation'] = self._participation
        info['num_tips']=self.num_tips

        return info


class Professor(Base):

    __tablename__ = 'professor'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    def __init__(self, last_name, first_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return "<Professor( '%d' , '%s' , '%s')>" % (self.id, self.first_name, self.last_name)


class Material(Base):

    __tablename__ = 'material'

    id = Column(String, primary_key=True)
    title = Column(String)
    prof_course = Column(Integer, ForeignKey('prof_course.id'))
    description = Column (String)
    year = Column(Integer)
    type = Column(String)
    file = Column(String)
    user_email = Column(String, ForeignKey('user.email'))

    def __init__(self, title, prof_course, description, year, type, file, user_email):
        self.title=title
        self.prof_course=prof_course
        self.description=description
        self.year=year
        self.type=type
        self.file=file
        self.user_email=user_email

    def __repr__(self):
        return "<Material( '%s' )>" % self.title


class Message(Base):

    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    sender_email = Column(String, ForeignKey('user.email'))
    receiver_email = Column(String, ForeignKey('user.email'))
    text = Column(String)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__ (self, sender_email, receiver_email, text):
        self.sender_email=sender_email
        self.receiver_email=receiver_email
        self.text=text

    def __repr__(self):
        return "<Message( '%s' , '%s')>" % (self.sender_email, self.receiver_email)


class Tip (Base):

    __tablename__ = 'tip'

    id = Column(Integer, primary_key=True)
    user_email = Column(String, ForeignKey ("user.email")) #
    prof_course = Column(Integer, ForeignKey("prof_course.id")) ##
    time = Column(String, default=current_time())
    _teaching = Column(Integer)
    _comprehension = Column(Integer)
    _availability = Column(Integer)
    _participation = Column(Integer)
    _material = Column(Integer)
    _books = Column(Integer)
    _attending = Column(Integer)
    _difficulty = Column(Integer)
    _time = Column(Integer)
    _result_rapidity = Column(Integer)
    note = Column(String)

    def __init__ (self, user_email, prof_course, _teaching, _comprehension, _availability, _participation, _material, _books, _attending, _difficulty, _time, _result_rapidity, note):
        self.user_email=user_email
        self.prof_course=prof_course
        self._teaching = _teaching
        self._comprehension=_comprehension
        self._availability = _availability
        self._participation = _participation
        self._material=_material
        self._books=_books
        self._attending=_attending
        self._difficulty=_difficulty
        self._time=_time
        self._result_rapidity=_result_rapidity
        self.note=note

        self.update_university_rating()

    def update_university_rating(self):
        user = User.query.filter(User.email==self.user_email).first()
        university = University.query.filter(University.name==user.university).first()
        university.update_rating(self.get_info())


    def __repr__(self):
        return "<Tip( '%d' , '%d' , '%s', '%s'  )>" % (self.id, self.prof_course, self.user_email, self.time)

    def get_info(self):
        info={}
        info['user_email']=self.user_email
        info['prof_course']=self.prof_course
        info['_teaching']=self._teaching
        info['_comprehension']=self._comprehension
        info['_availability']=self._availability
        info['_participation']=self._participation
        info['_material']=self._material
        info['_books']=self._books
        info['_attending']=self._attending
        info['_difficulty']=self._difficulty
        info['_time']=self._time
        info['_result_rapidity']=self._result_rapidity
        info['note']=self.note

        return info

class Tutoring_booking (Base):

    __tablename__ = 'tutoring_booking'

    id = Column (Integer, primary_key=True)
    request_email = Column(String, ForeignKey("user.email")) #
    offer_email = Column(String, ForeignKey("user.email")) #
    prof_course = Column(String, ForeignKey("prof_course.id")) ##
    interval_time = Column(String)

    def __init__ (self, request_email, offer_email, prof_course, interval_time):
        self.request_email=request_email
        self.offer_email=offer_email
        self.prof_course=prof_course
        self.interval_time=interval_time

    def __repr__(self):
        return "<Tutoring_booking( '%d' )>" % (self.id)

class Tutoring_offer (Base):

    __tablename__ = 'tutoring_offer'

    id = Column(Integer, primary_key=True)
    user_email = Column(String, ForeignKey("user.email")) #
    prof_course = Column(String, ForeignKey("prof_course.id")) ##
    interval_time = Column(String)
    type = Column(String)
    fare = Column(Float)

    def __init__(self, user_email, prof_course, interval_time, type, fare):
        self.user_email=user_email
        self.prof_course=prof_course
        self.interval_time=interval_time
        self.type=type
        self.fare=fare

    def __repr__(self):
        return "<Tutoring_offer( '%d' )>" % (self.id)

class User (Base):

    __tablename__ = 'user'

    email = Column(String, primary_key=True)
    is_logged = Column(String)##
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    university = Column(String, ForeignKey("university.name"))#
    faculty = Column(String)
    phone_number = Column(String)
    language = Column(String, ForeignKey("language.id"))#

    tips=relationship("Tip", cascade="all, delete-orphan")

    def __init__(self, email, password, first_name, last_name, university, faculty, phone_number, language):

        self.email=email
        self.password=password
        self.last_name=last_name
        self.first_name=first_name
        self.university=university
        self.faculty=faculty
        self.phone_number=phone_number
        self.language=language

    def __repr__(self):
        return "<User( '%s' , '%s' )>" % (self.email, self.university)

    def get_info (self):

        info = {}
        info['email']=self.email
        info['last_name']=self.last_name
        info['first_name']=self.first_name
        info['university']=self.first_name
        info['faculty']=self.faculty
        info['phone_number']=self.phone_number
        info['language']=self.language

        return info

    def add_tip(self, tip):
        self.tips.append(tip)

class Prof_Course (Base):

    __tablename__ = 'prof_course'

    id = Column (Integer, primary_key=True)
    prof_id = Column (Integer, ForeignKey("professor.id"))
    course_name = Column (String, ForeignKey("course.name"))

    def __repr__(self):
        return "<Prof_Course( '%d', '%s' , '%s' )>" % (self.id, self.prof_id, self.course_name)