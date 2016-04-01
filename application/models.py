from application import db

class Pam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deskId = db.Column(db.Integer, index=True, unique=False)
    classId = db.Column(db.Integer, index=True, unique=False)
    time = db.Column(db.DateTime, index=True, unique=False)
    tag = db.Column(db.String(128), index=True, unique=False)
    arousal = db.Column(db.Integer, index=True, unique=False)
    valence = db.Column(db.Integer, index=True, unique=False)
    na = db.Column(db.Integer, index=True, unique=False)
    pa = db.Column(db.Integer, index=True, unique=False)
    
    def __init__(self, deskId, classId, time, tag, arousal, valence, na, pa):
        self.deskId = deskId
        self.classId = classId
        self.time = time
        self.tag = tag
        self.arousal = arousal
        self.valence = valence
        self.na = na
        self.pa = pa

    def __repr__(self):
        return '<Pam %r>' % self.id

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=False)
    rows = db.Column(db.Integer, index=True, unique=False)
    columns = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, index=True, unique=False)
    sequential = db.Column(db.Boolean, index=True, unique=False)
    active = db.Column(db.Boolean, index=True, unique=False)

    def __init__(self, name, rows, columns, timestamp, sequential, active):
        self.name = name
        self.rows = rows
        self.columns = columns
        self.timestamp = timestamp
        self.sequential = sequential
        self.active = active

    def __repr__(self):
        return str(self.id)

class Desk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deskId = db.Column(db.Integer, index=True, unique=False)
    classId = db.Column(db.Integer, index=True, unique=False)
    row = db.Column(db.Integer, index=True, unique=False)
    column = db.Column(db.Integer, index=True, unique=False)
    enabled = db.Column(db.Boolean, index=True, unique=False)

    def __init__(self, deskId, classId, row, column, enabled=True):
        self.deskId = deskId
        self.classId = classId
        self.row = row
        self.column = column
        self.enabled = enabled

    def __repr__(self):
        return '<Desk %r>' % self.id

class Moonikin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, index=True, unique=False)
    time = db.Column(db.String(128), index=True, unique=False)
    valence = db.Column(db.Integer, index=True, unique=False)
    control = db.Column(db.Integer, index=True, unique=False)
    arousal = db.Column(db.Integer, index=True, unique=False)

    def __init__(self, uid, time, valence, control, arousal):
        self.uid = uid
        self.time = time
        self.valence = valence
        self.control = control
        self.arousal = arousal

    def __repr__(self):
        return '<Moonikin %r>' % self.uid

