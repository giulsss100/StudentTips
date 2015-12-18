from flask import Flask, render_template, request, make_response
import db_interaction
#TODO: come sono ordinati i tip? mi sembra che a volte me li ordini in maniera diversa
#TODO: avviso errori nel log in e avviso tip gia inserito
#TODO: altri possibili errori?

app = Flask(__name__)

"""Login or Signup"""


def login_user():
    if ('input_email' in request.form) and ('input_password' in request.form):
        user_mail = request.form['input_email']
        user_password = request.form['input_password']

        if ('input_firstname' in request.form):  # user is subscribing
            firstname = request.form['input_firstname']
            lastname = request.form['input_lastname']
            university = request.form['input_university']
            faculty = ''
            if ('input_faculty' in request.form):
                faculty = request.form['input_faculty']
            phone = ''
            if ('input_phone' in request.form):
                phone = request.form['input_phone']
            confirm_password = request.form['input_confirm_password']
            if not (str(user_password) == str(confirm_password)):
                return False
            else:
                db_interaction.insert_user(user_mail, user_password, firstname, lastname, university, faculty, phone)

        user = db_interaction.check_user(user_mail, user_password)
        return user
    return False


"""Cookie management AND logout: check if cookie exists, or user logged in"""


def cookie_status():
    # if cookie is not set
    if request.cookies.get('user') is None:
        return login_user()

    # otherwise cookie is already stored
    user_mail = request.cookies.get('user')
    user = db_interaction.get_user(user_mail)

    # check if the user has logged out
    if ('logout' in request.form):
        return False
    else:
        return user


"""Set the cookie"""


def cookie_setting(response_page, cookie_name, cookie_value):
    if cookie_value != False:
        if 'remember_me' in request.form:
            response_page.set_cookie(cookie_name, cookie_value, 3600 * 24 * 365 * 99)
        else:  # cookie available for just 5 minutes
            response_page.set_cookie(cookie_name, cookie_value, 60 * 5)
    else:  # unset the cookie
        response_page.set_cookie(cookie_name, '', 0)


"""Manage user cookie"""


def set_cookie_user(response):
    if cookie_status():
        cookie_setting(response, 'user', cookie_status().email)
    else:
        cookie_setting(response, 'user', False)
    return response


"""Average rating for a field (tips)"""


def avg_rating(tip_list, field):
    num_tips = len(tip_list)
    tot_stars = 0
    for tip_dict in tip_list.values():
        info = tip_dict['tip'].get_info()
        tot_stars = tot_stars + info[field]
    return int(tot_stars / num_tips)


"""Average rating of all fields"""


def tot_avg_rating(rating_list):
    tot_rating = 0
    for value in rating_list.values():
        tot_rating = tot_rating + value
    return int(tot_rating / len(rating_list))


def redirect_homepage():
    # redirect to homepage
    response = make_response(render_template('index.html', username=cookie_status(), title='Studentips'))
    if cookie_status():
        cookie_setting(response, 'user', cookie_status().email)
    else:
        cookie_setting(response, 'user', False)
    return response


@app.route('/', methods=['GET', 'POST'])
def homepage():
    login_successful = ''
    #check if login was successful
    if ('input_email' in request.form) and ('input_password' in request.form) and cookie_status():
        login_successful = True
    elif ('input_email' in request.form) and ('input_password' in request.form) and not cookie_status():
        login_successful = False
    response = make_response(render_template('index.html', username=cookie_status(), title='Studentips', login_successful=login_successful))
    return set_cookie_user(response)


@app.route('/login')
def login():
    response = make_response(render_template('login.html', username=cookie_status(), title='Studentips - Login'))
    return set_cookie_user(response)


@app.route('/signup')
def signup():
    response = make_response(render_template('signup.html', username=cookie_status(), title='Studentips - Signup'))
    return set_cookie_user(response)


@app.route('/course_tips', methods=['GET', 'POST'])
def course_tips():

    """if page accessed from address searchbar"""
    if not ('input_course' in request.form) and not ('input_professor' in request.form):
        return redirect_homepage()

    """Here we are sure the user has started a search for a course and a professor, or he has inserted a tip and wants to view the refreshed page"""
    input_course = request.form['input_course']
    input_professor = request.form['input_professor']

    if 'submit_tip' in request.form:
        """The user could have inserted a new tip"""

        prof_course = int(db_interaction.search_profcourse(input_course, input_professor))

        teaching = int(request.form['input_teaching'])
        comprehension = int(request.form['input_comprehension'])
        availability = int(request.form['input_availability'])
        participation = int(request.form['input_participation'])
        material = int(request.form['input_material'])
        books = int(request.form['input_books'])
        attending = int(request.form['input_attending'])
        difficulty = int(request.form['input_difficulty'])
        time = int(request.form['input_time'])
        result_rapidity = int(request.form['input_result_rapidity'])
        note = request.form['input_note']

        db_interaction.insert_tip(cookie_status().email, prof_course, teaching, comprehension, availability,
                                             participation, material, books, attending, difficulty, time,
                                             result_rapidity, note)


    """tip_list: dictionary of tips for the tuple (course, professor)"""
    tip_list = {}
    """rating_list: dictionary of average ratings for the tuple (course, professor)"""
    rating_list = {}
    """medium_rating: overall rating of the tuple (course, professor)"""
    medium_rating = ''

    """We first assume there aren't errors"""
    error = False

    """We first assume we can't tip"""
    can_tip = False

    course = db_interaction.search_course(input_course)
    prof = db_interaction.search_professor(input_professor)

    """check what is the wrong parameter the user passed as input"""
    if not course and prof:
        prof = prof.last_name + " " + prof.first_name
        error = 'Course %s has not been found.' % input_course
    elif not prof and course:
        course = course.name
        error = 'Professor %s has not been found.' % input_professor
    elif not prof and not course:
        error = 'Course: %s and Professor: %s have not been found.' % (input_course, input_professor)
    else:
        prof = prof.last_name + " " + prof.first_name
        course = course.name

        if not db_interaction.search_profcourse_tips(input_course, input_professor):
            error = 'No matches found for the couple COURSE: %s - PROFESSOR: %s' % (course, prof)
        else:
            for tip in db_interaction.search_profcourse_tips(input_course, input_professor):
                tip_ratings = {}
                tip_ratings['Quality of Teaching'] = tip._teaching
                tip_ratings['Comprehension of Course Objectives'] = tip._comprehension
                tip_ratings['Professor Availability'] = tip._availability
                tip_ratings['Participation of Students during lectures'] = tip._participation
                tip_ratings['Utility of academic Material'] = tip._material
                tip_ratings[
                    'Usefulness of Textbooks'] = tip._books  # ho dovuto cambiare il nome altrimenti non stampava le stelline colorate
                tip_ratings['Necessity to attend Lectures'] = tip._attending
                tip_ratings['Difficulty of the Exam'] = tip._difficulty
                tip_ratings['Time Availability at Exam'] = tip._time
                tip_ratings['Rapidity in receiving Exam Results'] = tip._result_rapidity

                """for each tip, we create an element containing info about the user, info about the tip itself and its ratings (to iterate on them)"""
                tip_list[db_interaction.get_user(tip.user_email)] = {'tip': tip, 'ratings': tip_ratings}

            if len(tip_list) > 0:
                rating_list['Quality of Teaching'] = avg_rating(tip_list, '_teaching')
                rating_list['Comprehension of Course Objectives'] = avg_rating(tip_list, '_comprehension')
                rating_list['Professor Availability'] = avg_rating(tip_list, '_availability')
                rating_list['Participation of Students during lectures'] = avg_rating(tip_list, '_participation')
                rating_list['Utility of academic Material'] = avg_rating(tip_list, '_material')
                rating_list['Usefulness of Textbooks'] = avg_rating(tip_list, '_books')
                rating_list['Necessity to attend Lectures'] = avg_rating(tip_list, '_attending')
                rating_list['Difficulty of the Exam'] = avg_rating(tip_list, '_difficulty')
                rating_list['Time Availability at Exam'] = avg_rating(tip_list, '_time')
                rating_list['Rapidity in receiving Exam Results'] = avg_rating(tip_list, '_result_rapidity')

                medium_rating = tot_avg_rating(rating_list)

            prof_course_id = db_interaction.search_profcourse(course, prof)

            if cookie_status() and not db_interaction.has_already_tipped(cookie_status().email, prof_course_id):
                can_tip = True

    response = make_response(
        render_template('view_course_tips.html', username=cookie_status(), title='Studentips - Course Tips',
                        medium_rating=medium_rating, rating_list=rating_list,
                        tip_list=tip_list, course=course, professor=prof, error=error, can_tip=can_tip))

    return set_cookie_user(response)


@app.route('/university_tips', methods=['GET', 'POST'])
def university_tips():
    """if page accessed from address searchbar"""
    if not ('input_university' in request.form):
        return redirect_homepage()

    """Here we are sure the user has started a search for a university"""
    university = request.form['input_university']

    university_db = db_interaction.search_university(university)

    """rating_list: list of average ratings for the university"""
    rating_list = {}

    if university_db:
        university_info = university_db.get_info()

        if (university_db.num_tips > 0):
            rating_list['Quality of Teaching'] = int(university_info['_quality'])
            rating_list['Professor Availability'] = int(university_info['_availability'])
            rating_list['Participation of Students during lectures'] = int(university_info['_difficulty'])
            rating_list['Difficulty of the Exam'] = int(university_info['_participation'])

    response = make_response(
        render_template('view_university_tip.html', username=cookie_status(), title='Studentips - University Tips',
                        rating_list=rating_list,
                        university=university_db))
    return set_cookie_user(response)


@app.route('/add_tip', methods=['GET', 'POST'])
def add_tip():
    course = request.form['input_course']
    professor = request.form['input_professor']

    response = make_response(
        render_template('add_tip.html', username=cookie_status(), title='Studentips - Add Tip', course=course,
                        professor=professor))

    return set_cookie_user(response)


@app.route('/wip', methods=['GET', 'POST'])
def wip():
    response = make_response(render_template('wip.html', username=cookie_status(), title='Studentips - Work in progress'))
    return set_cookie_user(response)


if __name__ == '__main__':
    app.run()
