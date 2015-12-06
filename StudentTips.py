from flask import Flask, render_template, request, make_response

app = Flask(__name__)

"""static folder is used for HTML, CSS and other static files
templates, instead, contains all dynamic folders

@app.rout('address in which we'll have to search')
def name of the page():
    return render.template('pageName.html',...)"""

def cookie_status(response_page, response_title):
    # look if there are cookies stored
    user_mail = request.cookies.get('user')
    #check if the user has logged out
    if('logout' in request.form):
        response = make_response(render_template(response_page, title=response_title, username=''))
        response.set_cookie('user', '', expires=0)
        return response
    #check if the user has logged in
    if (not user_mail) and ('input_email' in request.form) and ('input_password' in request.form):
        user_mail = request.form['input_email']
        user_password = request.form['input_password']
        # here we should include communication with DB, to check if credentials are correct
        """user = User.query.filter_by((email=user_email) & (password=user_password)).first()"""
        """update is_logged"""
        # in case of correct login, we set the cookies
        """response = make_response(render_template('index.html', title='Studentips', username=user.first_name))"""
        response = make_response(render_template(response_page, title=response_title, username=user_mail))
        if 'remember_me' in request.form: #wait for HTML for signed user to check if this is correct
            response.set_cookie('user', user_mail)
        return response
    elif not user_mail:
         return render_template(response_page, title=response_title, username='')

    return render_template(response_page, title=response_title, username=user_mail)


@app.route('/', methods=["POST", "GET"])
def homepage():
    #login and cookie management
    return cookie_status("index.html", "Studentips")

@app.route('/login')
def login():
    return render_template('login.html', title='Studentips - Login')

@app.route('/signup')
def signup():
    return render_template('signup.html', title='Studentips - Signup')

@app.route('/course_tips')
def course_tips():
    return render_template('view_course_tips.html', title='Studentips - Course Tips')



if __name__ == '__main__':
    app.run()
