from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "AutoService Manager работает!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("База данных создана!")
    app.run(debug=True)