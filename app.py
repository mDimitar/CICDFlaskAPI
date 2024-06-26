
from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    production_year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)


@app.route('/cars', methods=['GET'])
def get_all_cars():
    cars = Car.query.all()
    car_list = []
    for car in cars:
        car_data = {
            'id': car.id,
            'model': car.model,
            'manufacturer': car.manufacturer,
            'production_year': car.production_year,
            'price': car.price
        }
        car_list.append(car_data)
    return jsonify(car_list)


@app.route('/cars/add', methods=['POST'])
def create_car():
    data = request.get_json()
    new_car = Car(
        model=data['model'],
        manufacturer=data['manufacturer'],
        production_year=data['production_year'],
        price=data['price']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'message': 'Car created successfully! dimitar test'})


# Update an existing car
@app.route('/cars/edit/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    data = request.get_json()
    car.model = data['model']
    car.manufacturer = data['manufacturer']
    car.production_year = data['production_year']
    car.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Car updated successfully!'})


# Delete a car
@app.route('/cars/delete/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({'message': 'Car deleted successfully!'})


if __name__ == '__main__':
    app.run()
