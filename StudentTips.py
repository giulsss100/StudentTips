from datetime import datetime
from flask import Flask, render_template, request, make_response
import db_interaction

app = Flask(__name__)

"""Login or Signup"""
def login_user():
  if ('input_email' in request.form) and ('input_password' in request.form):
        user_mail = request.form['input_email']
        user_password = request.form['input_password']

        if('input_firstname' in request.form): #user is subscribing
            firstname = request.form['input_firstname']
            lastname = request.form['input_lastname']
            university = request.form['input_university']
            faculty = ''
            if('input_faculty' in request.form):
                faculty = request.form['input_faculty']
            phone = ''
            if('input_phone' in request.form):
                phone = request.form['input_phone']
            confirm_password = request.form['input_confirm_password']
            if not(str(user_password) == str(confirm_password)):
                return False
            else:
                db_interaction.insert_user(user_mail, user_password, firstname, lastname, university, faculty, phone)

        user = db_interaction.check_user(user_mail, user_password)
        return user
  return False


"""Cookie management AND logout: check if cookie exists, or user logged in"""
def cookie_status():
    #if cookie is not set
    if request.cookies.get('user') is None:
        return login_user()

    #otherwise cookie is already stored
    user_mail = request.cookies.get('user')
    user = db_interaction.get_user(user_mail)

    #check if the user has logged out
    if('logout' in request.form):
        return False
    else:
        return user

"""Set the cookie"""
def cookie_setting(response_page, cookie_name, cookie_value):
    if cookie_value != False:
        if 'remember_me' in request.form:
            response_page.set_cookie(cookie_name, cookie_value, 3600*24*365*99)
        else: #cookie available for just 5 minutes
            response_page.set_cookie(cookie_name, cookie_value, 60*5)
    else: #unset the cookie
        response_page.set_cookie(cookie_name, '', 0)

"""Average rating for a field (tips)"""
def avg_rating(tip_list, field):
    num_tips = len(tip_list)
    tot_stars = 0
    for tip in tip_list.values():
        info = tip.get_info()
        tot_stars = tot_stars + info[field]
    return int(tot_stars/num_tips)

"""Average rating of all fields"""
def tot_avg_rating(rating_list):
    tot_rating=0
    for value in rating_list.values():
        tot_rating=tot_rating+value
    return int (tot_rating/len(rating_list))


@app.route('/',methods=['GET', 'POST'])
def homepage():
    response=make_response(render_template('index.html', username=cookie_status(), title='Studentips'))
    if cookie_status():
        cookie_setting(response, 'user', cookie_status().email)
    else:
        cookie_setting(response, 'user', False)
    return response

@app.route('/login')
def login():
    response=make_response(render_template('login.html', username=cookie_status(), title='Studentips - Login'))
    if cookie_status():
        cookie_setting(response, 'user', cookie_status().email)
    else:
        cookie_setting(response, 'user', False)
    return response

@app.route('/signup')
def signup():
    response=make_response(render_template('signup.html', username=cookie_status(), title='Studentips - Signup'))
    if cookie_status():
        cookie_setting(response, 'user', cookie_status().email)
    else:
        cookie_setting(response, 'user', False)
    return response

@app.route('/course_tips', methods=['GET', 'POST'])
def course_tips():
    """Here we are sure the user has started a search for a course and a professor"""
    course = request.form['input_course']
    professor = request.form['input_professor']

    #1. RESEARCH THE COUPLE (COURSE, PROFESSOR)
    #2. IF IT EXISTS, GET THE ID OF THE COUPLE
    #3. SEARCH ALL THE TIPS HAVING THAT ID FOR COURSE, PROFESSOR
    #4. GET THE LIST OF TIPS AND SAVE IT TO tip_list

    #5. FOR EACH USER MAIL, GET USER

    """tip_list: dictionary of tips for the tuple (course, professor)"""
    tip_list = {}
    for tip in db_interaction.search_profcourse_tips(course, professor):
        tip_list[db_interaction.get_user(tip.user_email)] = tip

    """rating_list: dictionary of average ratings for the tuple (course, professor)"""
    rating_list = {}

    rating_list['Quality of Teaching'] = avg_rating(tip_list, '_teaching')
    rating_list['Comprehension of Course Objectives'] = avg_rating(tip_list, '_comprehension')
    rating_list['Professor Availability'] = avg_rating(tip_list, '_availability')
    rating_list['Participation of Students during lectures'] = avg_rating(tip_list, '_participation')
    rating_list['Utility of academic Material'] = avg_rating(tip_list, '_material')
    rating_list['Utility of Textbooks'] = avg_rating(tip_list, '_books')
    rating_list['Necessity to attend Lectures'] = avg_rating(tip_list, '_attending')
    rating_list['Difficulty of the Exam'] = avg_rating(tip_list, '_difficulty')
    rating_list['Time Availability at Exam'] = avg_rating(tip_list, '_time')
    rating_list['Rapidity in receiving Exam Results'] = avg_rating(tip_list, '_result_rapidity')

    medium_rating=tot_avg_rating(rating_list)


    response=make_response(render_template('view_course_tips.html', username=cookie_status(), title='Studentips - Course Tips',
                                           medium_rating=medium_rating, rating_list=rating_list,
                                           tip_list=tip_list ))
    if cookie_status():
        cookie_setting(response, 'user', cookie_status().email)
    else:
        cookie_setting(response, 'user', False)
    return response

@app.route('/university_tips',methods=['GET', 'POST'])
def university_tips():
    """Here we are sure the user has started a search for a university"""
    university = request.form['input_university']

    university_db = db_interaction.search_university(university)
    university_info = university_db.get_info()


    """rating_list: list of average ratings for the university"""
    rating_list = {}

    if(university_db.num_tips > 0):
        rating_list['Quality of Teaching'] = int(university_info['_quality'])
        rating_list['Professor Availability'] = int(university_info['_availability'])
        rating_list['Participation of Students during lectures'] = int(university_info['_difficulty'])
        rating_list['Difficulty of the Exam'] = int(university_info['_participation'])

    response=make_response(render_template('view_university_tip.html', username=cookie_status(), title='Studentips - University Tips', rating_list=rating_list,
                                           university=university_db ))
    if cookie_status():
        cookie_setting(response, 'user', cookie_status().email)
    else:
        cookie_setting(response, 'user', False)
    return response


if __name__ == '__main__':
    app.run()
