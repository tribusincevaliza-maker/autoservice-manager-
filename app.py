from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50))


@app.route('/')
def index():
    return "AutoService Manager работает!"


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("База данных создана!")
    app.run(debug=True)