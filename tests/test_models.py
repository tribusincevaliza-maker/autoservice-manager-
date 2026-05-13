import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

def test_create_client():
    with app.app_context():
        db.create_all()
        from app import Client
        client = Client(full_name="Тест", phone="123", email="test@test.com")
        db.session.add(client)
        db.session.commit()
        saved = Client.query.filter_by(phone="123").first()
        assert saved is not None
        print("✅ Тест пройден!")

if __name__ == '__main__':
    test_create_client()