from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
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
        #self.sort = sort.strip()
        self.tags = [Tag(text=tag.strip()) for tag in tags.split(',')]


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)

    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    message = db.relationship('Message', backref=db.backref('tags', lazy=True))

db.create_all()



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/main', methods=['GET','POST'])
def main():
    sort = Message.id
    #return render_template('main.html', messages=Message.query.all(), data1="abcd")
    #return render_template('main.html', messages=Message.query.order_by(Message.data1), data0="abcd")
    #return render_template('main.html', messages=Message.query.order_by(Message.id), data0="abcd")
    return render_template('main.html', messages=Message.query.order_by(sort), data0="abcd")


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag']
    data1 = request.form['data1']

    db.session.add(Message(text, tag, data1))
    db.session.commit()

    return redirect(url_for('main'))


@app.route('/sort/<name>', methods=['GET','POST'])#methods=['GET','POST']
def sort(name):
    if str(name) == "sort_by_data1":
        sort = Message.data1
    elif str(name) == "sort_by_text":
        sort = Message.text
    else:
        sort = Message.id

    return render_template('main.html', messages=Message.query.order_by(sort), data0="abcd")
