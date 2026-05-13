from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


# Модели
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50))
    cars = db.relationship('Car', backref='owner', lazy=True)


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    plate_number = db.Column(db.String(20))
    year = db.Column(db.Integer)


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Клиенты
@app.route('/clients')
def list_clients():
    clients = Client.query.all()
    return render_template('clients/list.html', clients=clients)


@app.route('/clients/add', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']

        new_client = Client(full_name=full_name, phone=phone, email=email)
        db.session.add(new_client)
        db.session.commit()

        return redirect(url_for('list_clients'))

    return render_template('clients/add.html')


# Автомобили
@app.route('/cars')
def list_cars():
    cars = Car.query.all()
    return render_template('cars/list.html', cars=cars)


@app.route('/cars/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        client_id = request.form['client_id']
        brand = request.form['brand']
        model = request.form['model']
        plate_number = request.form['plate_number']
        year = request.form['year'] or None

        new_car = Car(
            client_id=client_id,
            brand=brand,
            model=model,
            plate_number=plate_number,
            year=year
        )
        db.session.add(new_car)
        db.session.commit()

        return redirect(url_for('list_cars'))

    clients = Client.query.all()
    return render_template('cars/add.html', clients=clients)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("База данных создана!")
    app.run(debug=True)