from flask import Flask, render_template, request, make_response

app = Flask(__name__)

"""static folder is used for HTML, CSS and other static files
templates, instead, contains all dynamic folders

@app.rout('address in which we'll have to search')
def name of the page():
    return render.template('pageName.html',...)"""

def cookie_status(response_page, response_title):
    #if cookie is not set
    if request.cookies.get('user') is None:
        #check if the user has logged in
        if ('input_email' in request.form) and ('input_password' in request.form):
            user_mail = request.form['input_email']
            user_password = request.form['input_password']
            # here we should include communication with DB, to check if credentials are correct
            """user = User.query.filter_by((email=user_email) & (password=user_password)).first()"""
            """update is_logged"""
            # in case of correct login, we set the cookies
            """response = make_response(render_template('index.html', title='Studentips', username=user.first_name))"""
            response = make_response(render_template(response_page, title=response_title, username=user_mail))
            if 'remember_me' in request.form: #wait for HTML for signed user to check if this is correct
                response.set_cookie('user', user_mail, 3600*24*365*99)
            else: #cookie available for just 10 minutes
                response.set_cookie('user', user_mail, 60*10)
            return response

        return render_template(response_page, title=response_title, username='')

    #otherwise cookie is already stored
    user_mail = request.cookies.get('user')

    #check if the user has logged out
    if('logout' in request.form):
        response = make_response(render_template(response_page, title=response_title, username=''))
        response.set_cookie('user', '', 0)
        return response
    else:
        return render_template(response_page, title=response_title, username=user_mail)


@app.route('/', methods=["POST", "GET"])
def homepage():
    #login and cookie management
    return cookie_status('index.html', 'Studentips')

@app.route('/login')
def login():
    return cookie_status('login.html', 'Studentips - Login')

@app.route('/signup')
def signup():
    return cookie_status('signup.html', 'Studentips - Signup')

@app.route('/course_tips')
def course_tips():
    return cookie_status('view_course_tips.html', 'Studentips - Course Tips')



if __name__ == '__main__':
    app.run()
