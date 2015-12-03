from flask import Flask, render_template

app = Flask(__name__)

"""static folder is used for HTML, CSS and other static files
templates, instead, contains all dynamic folders

@app.rout('address in which we'll have to search')
def name of the page():
    return render.template('pageName.html',...)"""


@app.route('/')
def homepage():
    return render_template('index.html', title='Studentips')

@app.route('/login')
def login():
    return render_template('login.html', title='Studentips - Login')

@app.route('/signup')
def signup():
    return render_template('signup.html', title='Studentips - Signup')


#come faccio a passare dal form all'altra pagina??
@app.route('/formYourCourse')
def search_course_tips():
    return render_template('course_tips.html')



if __name__ == '__main__':
    app.run()
