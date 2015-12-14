from flask import Flask, render_template, request, make_response
from TipProvv import TipProvv

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
            faculty = request.form['input_faculty']
            phone = request.form['input_phone']
            confirm_password = request.form['input_confirm_password']
            return user_mail
            #if mail already in DB
            #return ''
            #if password and confirm password not corresponding
            #return ''
        else: #user is logging in
            # here we should include communication with DB, to check if credentials are correct
            """user = User.query.filter_by((email=user_email) & (password=user_password)).first()"""
            """update is_logged"""
            # in case of correct login, we set the cookies
            """response = make_response(render_template('index.html', title='Studentips', username=user.first_name))"""
            return user_mail
            #if controlli:
            #    return ''
  return ''


"""Cookie management AND logout: check if cookie exists, or user logged in"""
def cookie_status():
    #if cookie is not set
    if request.cookies.get('user') is None:
        return login_user()

    #otherwise cookie is already stored
    user_mail = request.cookies.get('user')

    #check if the user has logged out
    if('logout' in request.form):
        return ''
    else:
        return user_mail

"""Set the cookie"""
def cookie_setting(response_page, cookie_name, cookie_value):
    if cookie_value != '':
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
    for tip in tip_list:
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
    cookie_setting(response, 'user', cookie_status())
    return response

@app.route('/login')
def login():
    response=make_response(render_template('login.html', username=cookie_status(), title='Studentips - Login'))
    cookie_setting(response, 'user', cookie_status())
    return response

@app.route('/signup')
def signup():
    response=make_response(render_template('signup.html', username=cookie_status(), title='Studentips - Signup'))
    cookie_setting(response, 'user', cookie_status())
    return response

@app.route('/course_tips', methods=['GET', 'POST'])
def course_tips():
    """Here we are sure the user has started a search for a course and a professor"""

    #course = request.form['input_course']
    #professor = request.form['input_professor']

    #1. RESEARCH THE COUPLE (COURSE, PROFESSOR)
    #2. IF IT EXISTS, GET THE ID OF THE COUPLE
    #3. SEARCH ALL THE TIPS HAVING THAT ID FOR COURSE, PROFESSOR
    #4. GET THE LIST OF TIPS AND SAVE IT TO tip_list

    #5. FOR EACH USER MAIL, GET USER

    """tip_list: list of tips for the tuple (course, professor)"""
    tip_list = [] #from DB

    tip1 = TipProvv('16-12-2014 01:05', 'john.lennon@gmail.com', 'boh', 5, 2, 5, 1, 4, 2, 4, 5, 3, 2, 'Slides are the way.')
    tip2 = TipProvv('16-12-2014 01:05', 'paul.mccartney@gmail.com', 'boh', 5, 5, 5, 3, 3, 3, 4, 5, 4, 3, 'Ask the professor if you have problems.')
    tip3 = TipProvv('16-12-2014 01:05', 'george.harrison@gmail.com', 'boh', 5, 1, 3, 2, 3, 2, 4, 5, 1, 3, 'This course will destroy your life.')
    tip4 = TipProvv('16-12-2014 01:05', 'ringo.starr@gmail.com', 'boh', 5, 4, 4, 3, 5, 1, 3, 1, 3, 3, 'Easy. Cool.')

    tip_list.append(tip1)
    tip_list.append(tip2)
    tip_list.append(tip3)
    tip_list.append(tip4)

    """rating_list: list of average ratings for the tuple (course, professor)"""
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
     #course = request.form['input_course']
    #professor = request.form['input_professor']
    response=make_response(render_template('view_course_tips.html', username=cookie_status(), title='Studentips - Course Tips',
                                           medium_rating=medium_rating, rating_list=rating_list,
                                           tip_list=tip_list, course="Economics", professor="Cambini"))
    cookie_setting(response, 'user', cookie_status())
    return response

@app.route('/university_tips',methods=['GET', 'POST'])
def university_tips():
    """Here we are sure the user has started a search for a university"""
    #university = request.form['input_university']

    #1. RESEARCH USERS FOR THAT UNIVERSITY
    #2. ADD TIPS THEY GAVE

    #List of tips where the writer of the tip belong to the universtity searched
    tip_list = [] #from DB

    tip1 = TipProvv('16-12-2014 01:05', 'john.lennon@gmail.com', 'boh', 5, 2, 5, 1, 4, 2, 4, 5, 3, 2, 'Slides are the way.')
    tip2 = TipProvv('16-12-2014 01:05', 'paul.mccartney@gmail.com', 'boh', 5, 5, 5, 3, 3, 3, 4, 5, 4, 3, 'Ask the professor if you have problems.')
    tip3 = TipProvv('16-12-2014 01:05', 'george.harrison@gmail.com', 'boh', 5, 1, 3, 2, 3, 2, 4, 5, 1, 3, 'This course will destroy your life.')
    tip4 = TipProvv('16-12-2014 01:05', 'ringo.starr@gmail.com', 'boh', 5, 4, 4, 3, 5, 1, 3, 1, 3, 3, 'Easy. Cool.')

    tip_list.append(tip1)
    tip_list.append(tip2)
    tip_list.append(tip3)
    tip_list.append(tip4)


    """rating_list: list of average ratings for the university"""
    rating_list = {}

    rating_list['Quality of Teaching'] = avg_rating(tip_list, '_teaching')
    rating_list['Professor Availability'] = avg_rating(tip_list, '_availability')
    rating_list['Participation of Students during lectures'] = avg_rating(tip_list, '_participation')
    rating_list['Difficulty of the Exam'] = avg_rating(tip_list, '_difficulty')


    response=make_response(render_template('view_university_tip.html', username=cookie_status(), title='Studentips - University Tips', rating_list=rating_list,
                                           tip_list=tip_list ))
    cookie_setting(response, 'user', cookie_status())
    return response


@app.route('/add_tip', methods=['GET', 'POST'])
def add_tip():

    response=make_response(render_template('add_tip.html', username=cookie_status(), title='Studentips - Add Tip' ))
    return response


if __name__ == '__main__':
    app.run()
