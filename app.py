import BaseModel as BaseModel
from flask_sqlalchemy import SQLAlchemy
from libs.users import Users, get_password
from libs.car import Cars
from libs.message import Message
from flask import Flask, render_template, request, url_for, render_template, jsonify, redirect, session, Blueprint, flash, g
import os
import json
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from pip._vendor import requests
from libs.database import db_session
from sqlalchemy import asc, desc
from flask_httpauth import HTTPBasicAuth



SECRET_KEY = 333
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(BASE_FOLDER, "resources")


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
names = [["Mary", "../static/images/11.jpg", "../static/images/12.jpg", "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. ", "mnogobukv",789],
         ["Supercat", "../static/images/21.jpg", "../static/images/22.jpg", "Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa mollis.", "mnogobukv", 459],
         ["Kate", "../static/images/31.jpg", "../static/images/32.jpg", "mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv", "mnogobukv"],
         ["Name", "../static/images/41.jpg", "../static/images/42.jpg", "mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv ", "mnogobukv", 573],
         ["Name", "../static/images/51.jpg", "../static/images/52.jpg", "mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv ", "mnogobukv", 456]]
# users = {
#     "kira": generate_password_hash("tropp1"),
#     "susan": generate_password_hash("bye")
# }
sorts = ['sort_by_price', 'sort_by_name']


########################   verify_password   ########################
auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, hash_password):
    users = Users.get_users()
    # pas = db_session.query(Users).filter_by(login=username).one()
    # print(pas.password)
    if username in users and check_password_hash(get_password(username), hash_password):
        print(hash_password)
        print(username,get_password(username))
        return username

######################  remove db_session ###########################
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


###########################  1 PAGE   #################################
@app.route('/', methods=['GET'])
def index():
    sort = Cars.price
    return render_template('index.html', sorts=sorts, cars=db_session.query(Cars).order_by(sort))#(desc(sort))
    #, messages=Message.query.order_by(sort), data0=users[0]["login"].strip()


########################### page from_us ##############################
def json_reader():
    with open("C:/Users/i5/PycharmProjects/Site060606/Site_Flask/resourses/response.json") as f:
        user_data = (json.loads(f.read()).get("payload"))
    return user_data

@app.route('/from_us')
def from_us():
    return render_template('from_us.html', body = json_reader())


##########################   sign_in   #################################
@app.route('/sign_in')
@auth.login_required
def sign_in():
    sort = Cars.id
    #$return "Hello, {}!"#.format(auth.current_user())
    return render_template('index.html', sorts=sorts, cars=db_session.query(Cars).order_by(sort))#(desc(sort))


##########################   sign_up   #################################
# @app.route('/sign_up')
# @auth.login_required
# def sign_up():
#     # sort = Cars.price
#     return "Hello, {}!"#.format(auth.current_user())
# db.create_all()
# db.session.commit()

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
            #db_session.add(Users(login, generate_password_hash(password)))
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


###########################
@app.route('/main', methods=['GET','POST'])
def main():
    sort = Message.id
    return render_template('resourses/Old/main.html', names=names)#,  messages=Message.query.order_by(sort)


@app.errorhandler(404)
def page_not_found(error):
    return \
        render_template('page_not_found.html'), 404

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#

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
    #parser()
    app.run(host='127.0.0.1', port=5001, debug=True)
















#con = postgresql.open('pq://postgres:123@localhost:5432/site_flask')
#con.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, login CHAR(64), password CHAR(64))")

# ins = con.prepare("INSERT INTO users (login, password) VALUES ($1, $2)")
# # ins("afiskon", "123")
# ins("eax", "456")
# con.query("SELECT id, trim(login), trim(password) FROM users")
# users = con.query("SELECT * FROM users WHERE id = 1")
# print(users[0][0])
# print(users[0]["id"])
# print(users[0]["login"].strip())
# print(users[0]["password"].strip())
#
# def write_db(vendor_name):
#     # sql = """INSERT INTO vendors(vendor_name)VALUES(%s) RETURNING vendor_id;"""
#     con = None
#     vendor_id = None
#     #params = config()
#
#     cur.execute("INSERT INTO vendors (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3419, 'Abel', 17, 'Computer Science', 'ICT')")
#     #cur.execute(sql,(vendor_name))
#     vendor_id = cur.fetchone()[0]
#     con.commit()
#     cur.close()
#     # cur.execute("INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3419, 'Abel', 17, 'Computer Science', 'ICT')"
#     # )
#     # cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, login CHAR(64), password CHAR(64))")
#     # ins = cur.prepare("INSERT INTO users (login, password) VALUES ($1, $2)")
#     # ins("afiskon", "123")
#     # ins("eax", "456")
# write_db("vendor_name")

#-------------------------SELECT * FROM message LIMIT 50-------------------------
# with closing(psycopg2.connect(dbname='site_flask', user='postgres',
#                               password='123', host='localhost')) as conn:
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT * FROM message LIMIT 50')
#         for row in cursor:
#             print(row)
#------------------------------------------------------------------

# import psycopg2
# from psycopg2 import sql
# import postgresql
# from contextlib import closing

#--------------index---------------------
# num = request.args.get('num')
# if num:
#     session['data'] = dict(num=str(num), chord='0')
#     return redirect(url_for('user'))
#return render_template('from_us.html')

#----------------------------connect----------------------------------------------
# conn = psycopg2.connect(
#     database="site_flask",
#     user="postgres",
#     password="123",
#     host="localhost",
#     port="5432"
# )
#----------------INSERT INTO users (login, password)---------------------
# with conn.cursor() as cursor:
#     conn.autocommit = True
#     values =('PDX', 'Portland'),
#     insert = sql.SQL('INSERT INTO users (login, password) VALUES {}').format(sql.SQL(',').join(map(sql.Literal, values)))
#     cursor.execute(insert)
# cursor.close()
# conn.close()

#----------------SELECT * FROM users LIMIT 50---------------------
# with closing(psycopg2.connect(dbname='site_flask', user='postgres',
#                               password='123', host='localhost')) as conn:
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT * FROM users LIMIT 50')
#         for row in cursor:
#             print(row)
#========================================================================

#FOR_ELACTICSEARCH
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
#     with open("response.json") as f:
#         user_data =("%s" % (json.loads(f.read()).get("payload")))
#     return render_template('user.html', myfunction=json_reader(), user_json=user_data, data=list_id, img = ('../../'+list_id[1]),img2 = ('../../'+list_id[2]))
