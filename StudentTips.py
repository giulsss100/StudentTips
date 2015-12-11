from flask import Flask, render_template, request, make_response

app = Flask(__name__)

"""Login"""
def login_user():
  if ('input_email' in request.form) and ('input_password' in request.form):
        user_mail = request.form['input_email']
        user_password = request.form['input_password']
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
        else: #cookie available for just 10 minutes
            response_page.set_cookie(cookie_name, cookie_value, 60*10)
    else: #unset the cookie
        response_page.set_cookie(cookie_name, '', 0)


@app.route('/', methods=["POST", "GET"])
def homepage():
    response=make_response(render_template('index.html', username=cookie_status(), title='Studentips'))
    cookie_setting(response, 'user', cookie_status())
    return response

@app.route('/login', methods=["POST", "GET"])
def login():
    response=make_response(render_template('login.html', username=cookie_status(), title='Studentips - Login'))
    cookie_setting(response, 'user', cookie_status())
    return response

@app.route('/signup', methods=["POST", "GET"])
def signup():
    response=make_response(render_template('signup.html', username=cookie_status(), title='Studentips - Signup'))
    cookie_setting(response, 'user', cookie_status())
    return response


# classi create per testare la pagina course tip che pero per ora non funziona proprio parametrizzata in questo modo -> perche??
class Rating:
    def __init__(self, name, value):
        self.name=name
        self.value=value

class Tip:
    def __init__(self, user_email, time, note):
        self.user_email=user_email
        self.time=time
        self.note=note

@app.route('/course_tips', methods=["POST", "GET"])
def course_tips():


    #tip_list sara la lista di tip per quel corso, ottenuta con una query
    #tip_list=tips.query.filter(...) o qualcosa del genere

    tip1=Tip("giulia@hotmail.it","16-12-2014", "Commento" )
    tip_list=()
    rating1= Rating("Quality of teaching", 3)
    rating_list=()

    response=make_response(render_template('view_course_tips.html', username=cookie_status(), title='Studentips - Course Tips',tot_recensioni=20, medium_rate=3, rating_list=rating_list,
                                           tip_list=tip_list ))
    cookie_setting(response, 'user', cookie_status())
    return response


if __name__ == '__main__':
    app.run()
