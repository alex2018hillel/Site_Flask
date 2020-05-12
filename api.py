from flask import Flask, jsonify, make_response, request, url_for
from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth
# from flask_httpauth import HTTPDigestAuth
# from flask_httpauth import HTTPTokenAuth
parser = reqparse.RequestParser()
parser.add_argument("head")
parser.add_argument("link")
parser.add_argument("photo")
parser.add_argument("price")
from app import app
# app = Flask(__name__)
# api = Api(app)
# app.config['SECRET_KEY'] = '123'
auth = HTTPBasicAuth()


tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}

users = {
    "alex": "12345",
    "susan": "bye"
}

cars = [
    {"id": 1,"head": "Tesla Model X", "link": "https://www.autotrader.co.uk/classified/advert/202003178519443",
    "photo": "https://m.atcdn.co.uk/a/media/w260h196pd8d8d8/333af3baf2c84ef3b00192ce628fddd3.jpg", "price": 1484946},
    {"id": 2,"head": 'Tesla Model Y', "link": "https://www.autotrader.co.uk/classified/advert/202003178519443",
    "photo": "https://m.atcdn.co.uk/a/media/w260h196pd8d8d8/333af3baf2c84ef3b00192ce628fddd3.jpg", "price": 1484947},
    {"id": 3,"head": 'Tesla Model Z', "link": "https://www.autotrader.co.uk/classified/advert/202003178519443",
    "photo": "https://m.atcdn.co.uk/a/media/w260h196pd8d8d8/333af3baf2c84ef3b00192ce628fddd3.jpg", "price": 1484948}
]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1.0/cars', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'cars': cars})
    # return jsonify({'cars': map(make_public_task, cars)})

@app.route('/api/v1.0/cars/<int:car_id>', methods=['GET'])
def get_task(car_id):
    for car in cars:
        if(car_id == car['id']):
            return jsonify({'car': car})
    return "car not found", 404

@app.route('/api/v1.0/cars', methods=['POST'])
def create_task():
    if not request.json or not 'head' in request.json:
        abort(400)
    car = {
        'id': cars[-1]['id'] + 1,
        'head': request.json['head'],
        'photo': request.json.get('photo', ""),
        'link': request.json['link'],
        'price': request.json['price']
    }
    cars.append(car)
    return jsonify({'car': car}), 201

@app.route('/api/v1.0/cars/<int:car_id>', methods=['PUT'])
def update_task(car_id):
    args = parser.parse_args()
    if not request.json or not 'head' in request.json:
        abort(400)
    for car in cars:
        print(car)
        if (car["id"] +1) == car_id:
            car = {
                'id': car_id,
                'head': request.json['head'],
                'photo': request.json.get('photo', ""),
                'link': request.json['link'],
                'price':  request.json['price']
            }
            car["head"] = args["head"]
            car["link"] = args["link"]
            car["photo"] = args["photo"]
            car["price"] = args["price"]
            cars[car_id-1] = car
    return jsonify({'car': car}), 201

def make_public_task(car):
    new_car = {}
    for field in car:
        if field == 'id':
            new_car['uri'] = url_for('get_task', car_id=car['id'], _external=True)
        else:
            new_car[field] = car[field]
    return new_car


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return '12345'
    return None

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

# @auth.verify_token
# def verify_token(token):
#     if token in tokens:
#         return tokens[token]


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

if __name__ == '__main__':
    app.run(debug=True)


'''
curl http://localhost:5000//api/v1.0/cars
curl -i http://localhost:5000/api/v1.0/cars/2
curl -i -H "Content-Type: application/json" -X POST -d "{"id": 3,"head": 'Z', "link": "https://", "photo": "jpg", "price": 1484948}' http://localhost:5000//api/v1.0/cars
curl -i -H "Content-Type: application/json" -X POST -d "{"""head""": """Z""", """link""": """https://""", """photo""": """jpg""", """price""": 1484948}" http://localhost:5000//api/v1.0/cars

curl -u miguel:12345 -i http://localhost:5000/api/v1.0/cars

curl http://localhost:5000//api/v1/car3
curl http://localhost:5000//api/v1/car2 -X DELETE -v
curl http://localhost:5000//api/v1 -d "car=["head=5", "link=6", photo="7", "price=8"]" -X POST -v
curl http://localhost:5000//api/v1/car1 -d "head=5", "link=6", photo="7", "price=8" -X PUT -v
curl -i -X POST -H 'Content-Type: application/json' -d '{"data":{"head":"artist", "link":"Salvador Dali"}}' http://localhost:5000//api/v1/car1
'''