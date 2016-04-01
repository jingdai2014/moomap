from application import db
from application.models import Pam, Student, Moonikin

db.create_all()

print("DB created.")
