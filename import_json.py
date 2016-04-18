from application import db
from application.models import Pam, Desk, Classroom
import time
import datetime
import json
import sys

filename = sys.argv[1]
print "Reading data from "+filename+"."

with open(filename)as data_file:
	records = json.load(data_file)["pam"]

for r in records:
	pam_entered = Pam(int(r["desk"]), int(r["class"]), datetime.datetime.strptime(r["time"], "%a, %d %b %Y %H:%M:%S %Z"), r["tag"], int(r["arousal"]), int(r["valence"]), int(r["na"]), int(r["pa"]))
	db.session.add(pam_entered)

print "DB inserted."

db.session.commit()
db.session.close()