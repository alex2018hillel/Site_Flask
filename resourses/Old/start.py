from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:123@localhost:5433/auto1"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://myuser:123@localhost:5432/postgres"
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    data1 = db.Column(db.String(1024), nullable=False)

    def __init__(self, text, tags, data1):
        self.text = text.strip()
        self.data1 = data1.strip()
        # self.data1 = Data1(data=data1.strip())
        self.tags = [Tag(text=tag.strip()) for tag in tags.split(',')]


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)

    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    message = db.relationship('Message', backref=db.backref('tags', lazy=True))

# class Data1(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(32), nullable=False)
#
#     message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
#     message = db.relationship('Message', backref=db.backref('data1', lazy=True))

db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    # list = []
    # for message in Message.query.all():
    #     list0 = []
    #     for tag in message:
    #         list0.append(tag)
    #         print(tag)
    #     list.append(list0)
    return render_template('main.html', messages=Message.query.all(), data1="5678")
    # return render_template('main.html', messages=Message.query.order_by(Message.data1), data1="5678")


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag']
    data1 = request.form['data1']

    db.session.add(Message(text, tag, data1))
    db.session.commit()

    return redirect(url_for('main'))