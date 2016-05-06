import sqlite3
from flask import Flask, request, redirect, render_template, g, jsonify, flash, url_for, make_response
from contextlib import closing
import datetime
from application import db
from pytz import timezone

from application.models import Pam, Moonikin, Classroom, Desk
import collections
import random
from sqlalchemy import desc, and_

app = Flask(__name__)
app.secret_key = "poop" #sorry
app.config.from_object(__name__)

@app.route('/')
def home():

    classId = request.args.get('classId', '')
    # classId = int(request.form["classname"]) 
    deskId = request.args.get('deskId', '')

    if not classId and not deskId:
            classes = [(classroom.id, classroom.name) for classroom in Classroom.query.all()]

            return render_template('selectdesk.html', classes=classes, thisclass=0)
    else:
        if not deskId:
            classes = [(classroom.id, classroom.name) for classroom in Classroom.query.all()]
            thisclass = Classroom.query.filter_by(id=classId).first()
            desks = Desk.query.filter_by(classId=classId).all()
            desksDisabled = [d.deskId for d in desks if d.enabled is False]
            if thisclass.sequential:
                resp = make_response(redirect(url_for('home')))
                # resp.set_cookie('classId', str(classId))
                # resp.set_cookie('deskId', 'sequential')
                return resp
            else:
                return render_template('selectdesk.html', classes=classes, thisclass=classId, rows=thisclass.rows, columns=thisclass.columns, cname=thisclass.name, desks=desksDisabled)
        else:
        # classId = request.cookies.get('classId')
        # deskId  = request.cookies.get('deskId')

        # uid = request.cookies.get('uid')
            
            pam_seq = range(1, 17)
            random.shuffle(pam_seq)
            pam_seq = [str(i) for i in pam_seq]

            for ps in range(len(pam_seq)):
                pam_seq[ps] = pam_seq[ps] + "_" + str(random.randint(1, 3))

            pam_seq = pam_seq

            resp = make_response(render_template('pam.html', pam_seq=pam_seq, deskId=deskId, classId=classId))
            if deskId == 'sequential':
                firstDesk = Desk.query.filter_by(classId=int(classId)).order_by(Desk.deskId).first()
                resp = make_response(render_template('pam.html', pam_seq=pam_seq, deskId=firstDesk.deskId, classId=classId))
                resp.set_cookie('deskId', str(firstDesk.deskId))

            return resp

@app.route('/selectdesk', methods=['POST'])
def select_desk():
    classId = int(request.form["classname"])
    classes = [(classroom.id, classroom.name) for classroom in Classroom.query.all()]
    thisclass = Classroom.query.filter_by(id=classId).first()
    desks = Desk.query.filter_by(classId=classId).all()
    desksDisabled = [d.deskId for d in desks if d.enabled is False]
    if thisclass.sequential:
        resp = make_response(redirect(url_for('home', classId=classId, deskId='sequential')))
        # resp.set_cookie('classId', str(classId))
        # resp.set_cookie('deskId', 'sequential')
        return resp
    else:
        return render_template('selectdesk.html', classes=classes, thisclass=classId, rows=thisclass.rows, columns=thisclass.columns, cname=thisclass.name, desks=desksDisabled)

@app.route('/pam', methods=['POST'])
def pam():
    ids = request.form.keys()[0].split('-')

    
    classId = int(ids[0])
    # resp.set_cookie('classId', ids[0])
    c = Classroom.query.filter_by(id = classId).first()
    deskId = str(int(ids[2]) + int(ids[1])*c.columns)
    resp = make_response(redirect(url_for('home', classId=ids[0], deskId=deskId)))

    # resp.set_cookie('deskId', str(int(ids[2]) + int(ids[1])*c.columns))
    return resp

@app.route('/getcookie')
def get_cookie():
    uid = request.cookies.get('uid')
    if uid:
        return uid
    else:
        return 'user'

@app.route('/deletecookie')
def delete_cookie():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('classId', '')
    resp.set_cookie('deskId', '')
    return resp

@app.route('/add', methods=['POST'])
def pick_pam():
    pam_tags = [(1, 'afraid', 1, 4), (2, 'tense', 2, 4), (3, 'excited', 3, 4), (4, 'delighted', 4, 4), (5, 'frustrated', 1, 3), 
    (6, 'angry', 2, 3), (7, 'happy', 3, 3), (8, 'glad', 4, 3), (9, 'miserable', 1, 2), (10, 'sad', 2, 2), 
    (11, 'calm', 3, 2), (12, 'satisfied', 4, 2), (13, 'gloomy', 1, 1), (14, 'tired', 2, 1), (15, 'sleepy', 3, 1), 
    (16, 'serene', 4, 1)]

    if request.form['pam'] == '':
        current_pam = 10
    else:
        current_pam = int(request.form['pam'].split('_')[0])-1
    pam_tag = pam_tags[current_pam]
    PA = 4 * pam_tag[2] + pam_tag[3] - 4
    NA = 4 * (5 - pam_tag[2]) + pam_tag[3] - 4

    classId, deskId = request.form['classDesk'].split('-')
    # classId = request.cookies.get('classId')
    # deskId = request.cookies.get('deskId')

    pam_entered = Pam(int(deskId), int(classId), datetime.datetime.now(timezone('US/Eastern')), pam_tag[1], pam_tag[3], pam_tag[2], NA, PA)
    
    db.session.add(pam_entered)
    db.session.commit()        
    db.session.close()

    #return redirect(url_for('desk'))

    resp = make_response(redirect(url_for('thanks', classId=classId, deskId=deskId)))
    thisclass = Classroom.query.filter_by(id=int(classId)).first()
    if thisclass.sequential:
        desks = Desk.query.filter_by(classId=int(classId)).all()
        desksEnabled = [desk.deskId for desk in desks if desk.enabled]
        desksEnabled = sorted(desksEnabled)
        prevDesk = desksEnabled.index(int(deskId))
        if prevDesk == len(desksEnabled)-1:
            nextDesk = desksEnabled[0]
        else:
            nextDesk = desksEnabled[prevDesk+1]
        resp = make_response(redirect(url_for('thanks', classId=classId, deskId=str(nextDesk))))
        # resp.set_cookie('deskId', str(nextDesk))

    return resp

@app.route('/showpam')
def showpam():
    p = Pam.query.order_by(Pam.time)
    #p = Pam.query.order_by(Pam.username).limit(12).all()
    pams = []

    for pam_row in p:
        pam = {"id": pam_row.id, "class": pam_row.classId, "desk": pam_row.deskId, "time": pam_row.time, "tag": pam_row.tag, "arousal": pam_row.arousal, "valence": pam_row.valence, 
        "na": pam_row.na, "pa": pam_row.pa}
        pams.append(pam)

    return jsonify({"pam": pams}) 

@app.route('/classmap', methods=['POST'])
def classmap():
    heatmapData = post_heatmap(request)
    return render_template('classmap.html', pams=heatmapData[0], timeGroup=heatmapData[3], mapTime=heatmapData[4], classId=heatmapData[5])

@app.route('/heatmap', methods=['POST'])
def heatmap():
    heatmapData = post_heatmap(request)
    optType = request.form['optType']
    return render_template('heatmap.html', pams=heatmapData[0], rows=heatmapData[1], columns=heatmapData[2], classId=heatmapData[5], optType=optType)

@app.route('/selectclass')
def selectclass():
    classes = Classroom.query.all()
    classnames = [(c.id, c.name) for c in classes if c.active]

    return render_template('selectclass.html', classes = classnames)

@app.route('/registerclass')
def register():
    return render_template('register.html')

@app.route('/addclass', methods=['POST'])
def addclass():
    sequential = False
    if request.form.getlist('sequential'):
        sequential = True

    class_entered = Classroom(str(request.form['classname']), int(request.form['rownumber']), int(request.form['columnnumber']), datetime.datetime.now(timezone('US/Eastern')), sequential, True)
    db.session.add(class_entered)
    db.session.commit()
    disabled_classes = request.form['disabledclass'].split(',')
    
    db.session.refresh(class_entered)
    classId = int(str(class_entered))
    columns = int(request.form['columnnumber'])
    thisclass = Classroom.query.filter_by(id=classId).first()
    for i in range(thisclass.rows):
        for j in range(thisclass.columns):
            if str(i)+'-'+str(j) in disabled_classes:
                desk_entered = Desk(j + columns*i, classId, i, j, False)
            else:
                desk_entered = Desk(j + columns*i, classId, i, j, True)
            db.session.add(desk_entered)

    db.session.commit()  
    db.session.close()
    return render_template('selectclass.html')

@app.route('/modify')
def modify():
    classes = [(c.id, c.name) for c in Classroom.query.all() if c.active]

    return render_template('modifyclass.html', classes=classes, thisclass=0, name='-')

@app.route('/modifyclass', methods=['POST'])
def modifyclass():
    classId = int(request.form["oldclass"])
    classes = [(c.id, c.name) for c in Classroom.query.all()]
    thisclass = Classroom.query.filter_by(id=classId).first()

    desks = Desk.query.filter_by(classId=classId).all()
    disabledDesks = [str(d.row)+'-'+str(d.column) for d in desks if d.enabled is False]
    return render_template('modifyclass.html', classes=classes, thisclass=classId, name=thisclass.name, rows=thisclass.rows, columns=thisclass.columns, disabledDesks=disabledDesks, sequential=thisclass.sequential)

@app.route('/confirmmodify', methods=['POST'])
def confirmmodify():
    classId = int(request.form["oldclass"])
    oldClass = Classroom.query.filter_by(id=classId).first()
    oldDisabledClasses = request.form['olddisabledclass'].split(',')[:-1]

    newClassName = str(request.form['classname'])
    newClassRow = int(request.form['rownumber'])
    newClassColumn = int(request.form['columnnumber'])
    newDisabledClasses = request.form['disabledclass'].split(',')[:-1]
    newSequential = False
    if request.form.getlist('sequential'):
        newSequential = True

    if oldClass.rows == newClassRow and oldClass.columns == newClassColumn:
        if oldDisabledClasses != newDisabledClasses:
            for odc in oldDisabledClasses:
                Desk.query.filter_by(classId=classId, row=odc.split('-')[0], column=odc.split('-')[1]).update({"enabled": True})
            for ndc in newDisabledClasses:
                Desk.query.filter_by(classId=classId, row=ndc.split('-')[0], column=ndc.split('-')[1]).update({"enabled": False})
            if oldClass.name != newClassName:
                Classroom.query.filter_by(id=classId).update({"name": newClassName})
            if oldClass.sequential != newSequential:
                Classroom.query.filter_by(id=classId).update({"sequential": newSequential})
        else:
            if oldClass.name != newClassName:
                Classroom.query.filter_by(id=classId).update({"name": newClassName})
            if oldClass.sequential != newSequential:
                Classroom.query.filter_by(id=classId).update({"sequential": newSequential})
    else:
        Classroom.query.filter_by(id=classId).update({"active": False})
        class_entered = Classroom(str(request.form['classname']), int(request.form['rownumber']), int(request.form['columnnumber']), datetime.datetime.now(timezone('US/Eastern')), newSequential, True)
        db.session.add(class_entered)
        db.session.commit()
        
        db.session.refresh(class_entered)
        newClassId = int(str(class_entered))
        columns = int(request.form['columnnumber'])
        thisclass = Classroom.query.filter_by(id=newClassId).first()
        for i in range(thisclass.rows):
            for j in range(thisclass.columns):
                if str(i)+'-'+str(j) in newDisabledClasses:
                    desk_entered = Desk(j + columns*i, newClassId, i, j, False)
                else:
                    desk_entered = Desk(j + columns*i, newClassId, i, j, True)
                db.session.add(desk_entered)

    db.session.commit()  
    db.session.close()
    
    resp = make_response(redirect(url_for('selectclass')))
    return resp

"""
@app.route('/moonikins')
def moonikins():
    uid = request.cookies.get('uid')

    if uid:
        student_name = Student.query.filter_by(id=int(uid)).first().fname
        return render_template('moonikins.html', name=student_name, uid=uid)

    else:
        s = Student.query.all()
        students = []

        for student_row in s:
            student = (student_row.id, student_row.fname + " " + student_row.lname)
            students.append(student)

        students = sorted(students, key=lambda x: x[1])

        return render_template('selectuser.html', students=students, total=len(students))

@app.route('/addmoonikin', methods=['POST'])
def add_moonikin():
    valence = int(request.form['valence'])
    control = int(request.form['control'])
    arousal = int(request.form['arousal'])
    moonikin_entered = Moonikin(int(request.form['uid']), str(datetime.datetime.now(timezone('US/Eastern'))), valence, control, arousal)
        
    db.session.add(moonikin_entered)
    db.session.commit()        
    db.session.close()

    return redirect(url_for('moonikins'))  

@app.route('/showmoonikins')
def show_moonikins():
    m = Moonikin.query.all()
    moonikins = []

    for m_row in m:
        moonikin = {"uid": m_row.uid, "time": m_row.time, "valence": m_row.valence, "control": m_row.control, "arousal": m_row.arousal}
        moonikins.append(moonikin)

    return jsonify({"moonikins": moonikins}) 
"""
@app.route('/soundmap')
def sound():
    return render_template('soundmap.html')

@app.route('/thanks')
def thanks():
    classId = request.args.get('classId', '')
    deskId = request.args.get('deskId', '')
    thisclass = Classroom.query.filter_by(id=int(classId)).first()
    if thisclass.sequential:
        sequential = 'sq'
    else:
        sequential = 'nsq'
    return render_template('thanks.html', classId=classId, deskId=deskId, sequential=sequential)

def redirect_url(default='home'):
    return request.args.get('home') or \
           request.referrer or \
           url_for(default)

def post_heatmap(req):
    classId = req.form['classid']
    c = Classroom.query.filter_by(id = int(classId)).first()
    p = Pam.query.filter_by(classId = int(classId)).order_by(desc(Pam.time))
    pamTime = [pt.time for pt in p]
    timeGroup = []
    for pt in pamTime:
        if not timeGroup:
            timeGroup.append(pt)
            continue
        if pt < timeGroup[-1] - datetime.timedelta(minutes = 10):
            timeGroup.append(pt)

    timeGroup = [(tg.strftime("%B %d, %Y - %H:%M").replace(" ", "_"), tg.strftime("%B %d, %Y - %H:%M")) for tg in timeGroup]
    # return str(datetime.datetime.strptime(timeGroup[0], "%B %d, %Y - %H:%M") - datetime.timedelta(minutes = 10))
    # if not request.form['time']:
    try:
        mapTime = req.form['time'].replace("_", " ")
    except:
        mapTime = timeGroup[0][1]

    timeline = datetime.datetime.strptime(mapTime, "%B %d, %Y - %H:%M") - datetime.timedelta(minutes = 10)
    pclass = Pam.query.filter(Pam.classId == int(request.form['classid'])).filter(Pam.time >= timeline).all()

    pams = []
    deskids = []
    for pam_row in pclass:
        # get only the most recent record for each deskId
        if (pam_row.deskId in deskids):
            continue
        pam = {"deskId": pam_row.deskId, "time": pam_row.time, "tag": pam_row.tag, "arousal": pam_row.arousal, "valence": pam_row.valence, 
        "na": pam_row.na, "pa": pam_row.pa}
        pams.append(pam)
        deskids.append(pam_row.deskId)

    del deskids

    return ({"pam": pams}, c.rows, c.columns, timeGroup, mapTime, classId)
    # return render_template(url, pams={"pam": pams}, rows=c.rows, columns=c.columns, timeGroup=timeGroup, mapTime=mapTime, classId=classId)

if __name__ == '__main__':
	app.run(debug=True)
	# connect_db()
	# init_db()

