from application import db
from application.models import Pam, Moonikin, Desk, Classroom
import random, datetime


db.drop_all()
db.create_all()

# students = ["Muhammad Khadafi", "Lexus Dai", "Xiaoyang Ma", "Jonathan Huang", "Rohit Jain", "Joanna Zhang", "Alap Parikh", "Brandon Plaster", "Daniel Levine", "Shawn Bramson", "Sean Herman", "Oliver Hoffman", "Inna Shteinbuk", "Yeehan Chan", "Hannah Xue", "Jean Lin", "Huai-Che Lu", "Praveen Gupta", "Omri Sass", "Zaid Haque"]
# print len(students)
row = column = 0

pam_tags = [(1, 'afraid', 1, 4), (2, 'tense', 2, 4), (3, 'excited', 3, 4), (4, 'delighted', 4, 4), (5, 'frustrated', 1, 3), 
(6, 'angry', 2, 3), (7, 'happy', 3, 3), (8, 'glad', 4, 3), (9, 'miserable', 1, 2), (10, 'sad', 2, 2), 
(11, 'calm', 3, 2), (12, 'satisfied', 4, 2), (13, 'gloomy', 1, 1), (14, 'tired', 2, 1), (15, 'sleepy', 3, 1), 
(16, 'serene', 4, 1)]

classroom_entered = Classroom("Intro to CM", 4, 3, datetime.datetime.now(), sequential=True, active=True)
# print classroom_entered

db.session.add(classroom_entered)
db.session.commit() 
db.session.refresh(classroom_entered)

# print int(str(classroom_entered))
classId = int(str(classroom_entered))

for i in range(4):
	for j in range(3):
		if j%2 == 0:
			desk_entered = Desk(j + 3*i, classId, i, j, True)
		else:
			desk_entered = Desk(j + 3*i, classId, i, j, False)
		db.session.add(desk_entered)

db.session.commit() 

print Desk.query.all()

"""
for desk in range(12):
	deskId = column + 3*row
	random_pam = random.randint(0, 15)
	#random_pam = 0
	pam_tag = pam_tags[random_pam]
	PA = 4 * pam_tag[2] + pam_tag[3] - 4
	NA = 4 * (5 - pam_tag[2]) + pam_tag[3] - 4

	pam_entered = Pam(deskId, classId, datetime.datetime.now(), pam_tag[1], pam_tag[3], pam_tag[2], NA, PA)
	db.session.add(pam_entered)

	column += 1
	if column > 3:
		row += 1
		column = 0


for desk in range(12):
	deskId = column + 3*row
	#random_pam = random.randint(0, 15)
	random_pam = 4
	pam_tag = pam_tags[random_pam]
	PA = 4 * pam_tag[2] + pam_tag[3] - 4
	NA = 4 * (5 - pam_tag[2]) + pam_tag[3] - 4

	pam_entered = Pam(deskId, classId, datetime.datetime.now()-datetime.timedelta(minutes=10), pam_tag[1], pam_tag[3], pam_tag[2], NA, PA)
	db.session.add(pam_entered)

	column += 1
	if column > 3:
		row += 1
		column = 0
"""

db.session.commit()        
db.session.close()




print Pam.query.all()
print [c.name for c in Classroom.query.group_by(Classroom.name)]











# 	did = column + 4*row
# 	desk_entered = Desk(did)
# 	db.session.add(desk_entered)

# 	random_pam = random.randint(0, 15)
# 	pam_tag = pam_tags[random_pam]
# 	PA = 4 * pam_tag[2] + pam_tag[3] - 4
# 	NA = 4 * (5 - pam_tag[2]) + pam_tag[3] - 4

# 	pam_entered = Pam(did, str(datetime.datetime.now()), pam_tag[1], pam_tag[3], pam_tag[2], NA, PA)
# 	db.session.add(pam_entered)

# 	column += 1
# 	if column > 3:
# 		row += 1
# 		column = 0

# db.session.commit()        
# db.session.close()

print("Test DB created.")

