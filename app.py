from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import date

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


# ==================== МОДЕЛИ ====================

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


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50))
    phone = db.Column(db.String(20))


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    problem_description = db.Column(db.Text)
    status = db.Column(db.String(50), default='В работе')
    total_price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.Date)


# ==================== ГЛАВНАЯ ====================

@app.route('/')
def index():
    return render_template('index.html')


# ==================== КЛИЕНТЫ ====================

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


# ==================== АВТОМОБИЛИ ====================

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


# ==================== ЗАКАЗЫ ====================

@app.route('/orders')
def list_orders():
    orders = Order.query.all()
    return render_template('orders/list.html', orders=orders)


@app.route('/orders/add', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        client_id = request.form['client_id']
        car_id = request.form['car_id']
        employee_id = request.form.get('employee_id') or None
        problem_description = request.form['problem_description']
        total_price = request.form['total_price']

        new_order = Order(
            client_id=client_id,
            car_id=car_id,
        employee_id = employee_id,
        problem_description = problem_description,
        total_price = total_price,
        created_at = date.today()
        )
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('list_orders'))

    clients = Client.query.all()
    employees = Employee.query.all()
    return render_template('orders/add.html', clients=clients, employees=employees)


@app.route('/get_cars/<int:client_id>')
def get_cars(client_id):
    cars = Car.query.filter_by(client_id=client_id).all()
    return jsonify([{'id': c.id, 'brand': c.brand, 'model': c.model, 'plate_number': c.plate_number} for c in cars])


@app.route('/orders/<int:order_id>/status', methods=['POST'])
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = request.form['status']
    db.session.commit()
    return redirect(url_for('list_orders'))


# ==================== ЗАПУСК ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("База данных создана!")
    app.run(debug=True)