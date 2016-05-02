from application import db
from application.models import Pam

user = Pam.query.filter_by(deskId=9).all()
print len(user)
# for u in user:
# 	db.session.delete(u)
# # db.session.delete(user)
# db.session.commit()
# user.uid = 18
# db.session.commit()