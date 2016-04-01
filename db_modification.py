from application import db
from application.models import Colors

user = Colors.query.get(69)
print user.uid
# user.uid = 18
# db.session.commit()