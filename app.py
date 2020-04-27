from flask_sqlalchemy import SQLAlchemy
from parse_olx import Cars, parser
from flask import Flask, render_template, request, url_for, jsonify, redirect, session, g
import os
import json
from pip._vendor import requests

SECRET_KEY = 333
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(BASE_FOLDER, "resources")

app = Flask(__name__)
names = [["Mary", "../static/images/11.jpg", "../static/images/12.jpg", "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. ", "mnogobukv",789],
         ["Supercat", "../static/images/21.jpg", "../static/images/22.jpg", "Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa mollis.", "mnogobukv", 459],
         ["Kate", "../static/images/31.jpg", "../static/images/32.jpg", "mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv", "mnogobukv"],
         ["Name", "../static/images/41.jpg", "../static/images/42.jpg", "mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv ", "mnogobukv", 573],
         ["Name", "../static/images/51.jpg", "../static/images/52.jpg", "mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv mnogobukv ", "mnogobukv", 456]]


POSTGRES = {
    'user': 'postgres',
    'pw': '123',
    'db': 'site_flask',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' %POSTGRES
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:123@localhost:5432/site_flask"
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    data1 = db.Column(db.String(1024), nullable=False)

    def __init__(self, text, tags, data1, sort="Message.text"):
        self.text = text.strip()
        self.data1 = data1.strip()
        self.tags = [Tag(text=tag.strip()) for tag in tags.split(',')]


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)

    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    message = db.relationship('Message', backref=db.backref('tags', lazy=True))

db.create_all()

@app.route('/', methods=['GET'])
def index():
    sort1 = Message.id
    sort = Cars.id
    return render_template('index.html', names=names, cars=Cars.query.order_by(sort), messages=Message.query.order_by(sort1))#, messages=Message.query.order_by(sort), data0=users[0]["login"].strip()

@app.route('/main', methods=['GET','POST'])
def main():
    sort = Message.id
    return render_template('main.html', names=names, messages=Message.query.order_by(sort))#, data0=users[0]["login"].strip()

@app.route('/from_us')
def from_us():
    return render_template('from_us.html', body = json_reader())

@app.route('/user')
def user():
    with open("response.json") as f:
        user_data =("%s" % (json.loads(f.read()).get("payload")))
        #return render_template('user.html', myfunction=search, user_json =user_data,  data=session.get('data') or {'num': 1, 'chord': '0'}) #u = 'User %s' % username,
        return render_template('game.html', myfunction=json_reader(), user_json =user_data, data=session.get('data') or {'num': 'cghfgh', 'chord': '0'})

@app.route('/user/<index>/', methods=['POST'])
def doit(index):
    print(index)
    list = []
    for i in names:
        list.append(i[0])
        sort_list = sorted(list)

    list_id = [l for l in names if l[0] == index][0]
    print('')
    print(list_id)
    with open("resourses/response.json") as f:
        user_data =("%s" % (json.loads(f.read()).get("payload")))
    return render_template('user.html', myfunction=json_reader(), user_json=user_data, data=list_id, img = ('../../'+list_id[1]),img2 = ('../../'+list_id[2]))

app.secret_key = '73870e7f-634d-433b-946a-8d20132bafac'

@app.route('/', methods=['POST'])
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


def json_reader():
    with open("response.json") as f:
        user_data = (json.loads(f.read()).get("payload"))
    return user_data

json_reader()

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

@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag']
    data1 = request.form['data1']

    db.session.add(Message(text, tag, data1))
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/sort/<name>', methods=['GET','POST'])#methods=['GET','POST']
def sort(name):
    if str(name) == "sort_by_name":
        sort = Cars.head
    elif str(name) == "sort_by_price":
        sort = Cars.price
    else:
        sort = Cars.id

    return render_template('index.html', names=names, cars=Cars.query.order_by(sort), data0="abcd")


if __name__ == '__main__':
    parser()
    app.run(host='127.0.0.1', port=5000)
















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
