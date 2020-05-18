import BaseModel as BaseModel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from libs.users import Users, get_password
from libs.car import Cars
from libs.message import Message
from flask import Flask, request, url_for, render_template, jsonify, redirect, flash
import os
import json
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from pip._vendor import requests
from libs.database import db_session
from flask_httpauth import HTTPBasicAuth
from flask import current_app as app

SECRET_KEY = 333
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(BASE_FOLDER, "resources")


# app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
sorts = ['sort_by_price', 'sort_by_name']

########################   verify_password   ########################

auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, hash_password):
    users = Users.get_users()
    if username in users and check_password_hash(get_password(username), hash_password):
        print(hash_password)
        print(username,get_password(username))
        return username

######################  remove db_session ###########################

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

###########################  1 PAGE   ###############################

@app.route('/', methods=['GET'])
def index():
    sort = Cars.price
    return render_template('index.html', sorts=sorts, cars=db_session.query(Cars).order_by(sort))#(desc(sort))

########################## page from_us #############################

def json_reader():
    with open("C:/Users/i5/PycharmProjects/Site060606/Site_Flask/resourses/response.json") as f:
        user_data = (json.loads(f.read()).get("payload"))
    return user_data

@app.route('/from_us')
def from_us():
    return render_template('from_us.html', body = json_reader())

##########################   sign_in   #############################

@app.route('/sign_in')
@auth.login_required
def sign_in():
    sort = Cars.id
    #$return "Hello, {}!"#.format(auth.current_user())
    return render_template('index.html', sorts=sorts, cars=db_session.query(Cars).order_by(sort))#(desc(sort))

##########################   sign_up   #############################

@app.route('/sign_up', methods=("GET", "POST"))
def sign_up():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        error = None
        if not login:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (db_session.query(Users).filter_by(login=login).first()is not None):
            error = f"User {login} is already registered."

        if error is None:
            db_session.add(Users(login, generate_password_hash(password)))
            db_session.commit()
            return redirect(url_for("index"))
        flash(error)

    return render_template("sign_up.html")

##################  second page  #################################

@app.route('/old_car')
@auth.login_required
def old_car():
    message_sort = Message.text
    sort = Cars.id
    return render_template('index1.html', sorts=sorts, cars=db_session.query(Cars).order_by(sort),
                           messages=db_session.query(Message).order_by(message_sort))#(desc(sort))

#####################   sort_car   ################################

@app.route('/sort_car', methods=['GET', 'POST'])
def sort_car():
    app.logger.info(request)
    if request.method == 'POST':
        sort = Cars.id
        if request.form['sort'] == 'sort_by_name':
            sort = Cars.head
            print(sort)
        elif request.form['sort'] == 'sort_by_price':
            sort = Cars.price
            print(sort)
        return render_template('index.html', sorts=sorts, cars=db_session.query(Cars).order_by(sort))#(desc(sort))
    else:
        sort = Cars.price
        return render_template('index.html', sorts=sorts, cars=db_session.query(Cars).order_by(sort))#(desc(sort))

#######################   add_message   #########################

@app.route('/add_message', methods=['GET', 'POST'])
@auth.login_required
def add_message():
    message_sort = Message.id
    if request.method == 'POST':
        text = request.form['text']
        data1 = request.form['data1']
        db_session.add(Message(text, data1))
        db_session.commit()
        return render_template('add_message.html', sorts=sorts, messages=db_session.query(Message).order_by(message_sort))
        # return render_template('index.html', sorts=sorts, cars=db_session.query(Cars).order_by(sort))#(desc(sort))
    else:
        return render_template('add_message.html', sorts=sorts, messages=db_session.query(Message).order_by(message_sort))

######################   sort message  #########################

@app.route('/sort/<name>', methods=['GET'])
def sort(name):
    if str(name) == "sort_by_text":
        message_sort = Message.text
    elif str(name) == "sort_by_data1":
        message_sort = Message.data1
    else:
        message_sort = Message.id
    return render_template('add_message.html', sorts=sorts, messages=db_session.query(Message).order_by(message_sort))

###############################################################

@app.route('/main', methods=['GET','POST'])
def main():
    sort = Message.id
    return render_template('resourses/Old/main.html', )#,  messages=Message.query.order_by(sort), names=names


@app.errorhandler(404)
def page_not_found(error):
    return \
        render_template('page_not_found.html'), 404

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  FINAL  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#





































@app.route('/user/<username>')
def show_user_profile(username):
    with open("response.json") as f:
        user_data =("%s" % (json.loads(f.read()).get("payload")))
        #return "%s - %s" % (json.loads(f.read()).get("payload"))
        return render_template('user.html', myfunction=json_reader(), user_json =user_data, u = 'User %s' % username)# 'User %s' % username


@app.route('/api/save-image/')
def add_data_handler():
    if request.form.get('secret'):
        category = request.form.get('category')
        image = request.files.get('image')

        return jsonify(dict(success=1))

    return jsonify(dict(success=0))

with app.test_request_context():
    print(url_for('from_us'))
    print(url_for('index'))

# @app.route('/main', methods=['GET','POST'])
# def main():
#     sort = Message.id
#     return render_template('main.html', names=names, messages=Message.query.order_by(sort), data0=users[0]["login"].strip())
#

# @app.route('/user/<index>/', methods=['POST'])
# def doit(index):
#     print(index)
#     list = []
#     for i in names:
#         list.append(i[0])
#         sort_list = sorted(list)
#
#     list_id = [l for l in names if l[0] == index][0]
#     print('')
#     print(list_id)
#     with open("resourses/response.json") as f:
#         user_data =("%s" % (json.loads(f.read()).get("payload")))
#     return render_template('user.html', myfunction=json_reader(), user_json=user_data, data=list_id, img = ('../../'+list_id[1]),img2 = ('../../'+list_id[2]))
#
# app.secret_key = '73870e7f-634d-433b-946a-8d20132bafac'


@app.route('/post', methods=['POST'])
def index_post():
    print("methods=['POST']")
    category = request.form.get('category')
    image = request.files.get('image')

    if category in ['programming', 'text']:
        req = requests.request(
            method='POST',
            url='http://127.0.0.1:5001/api/save-image/',
            files=dict(
                image=(
                    image.filename,
                    image.stream,
                    image.mimetype
                )
            ),
            data=dict(
                category=category,
                secret=SECRET_KEY
            )
        )

        if req.status_code == requests.codes.ok:
            data = req.json()
            print(data)




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)



