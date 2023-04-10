from . import db
from werkzeug.security import generate_password_hash

def initDatabase():
    from .models import User
    myAdmin = User(email="admin@default", first_name="admin", password=generate_password_hash("aa", method='sha256'), is_admin=True)
    db.session.add(myAdmin)
    db.session.commit()
    print("added admin!")