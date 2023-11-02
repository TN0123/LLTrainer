from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///times.db'
db = SQLAlchemy(app)

class TimeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    caseIndex = db.Column(db.Integer)
    timeValue = db.Column(db.Integer)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def index():
    times = TimeRecord.query.with_entities(TimeRecord.content, TimeRecord.id).order_by(TimeRecord.id.desc()).all()
    time_records = TimeRecord.query.all()
    case_times = {}
    pllNames = ["Aa", "Ab", "E", "F", "Ga", "Gb", "Gc", "Gd", "H", "Ja", "Jb", "Na", "Nb", "Ra", "Rb", "T", "Ua", "Ub", "V", "Y", "Z"]

    for record in time_records:
        case = record.caseIndex
        time_value = record.timeValue
        time = record.content
        
        if case not in case_times:
            case_times[case] = (time_value, time)
        else:
            if time_value is not None and (case_times[case][0] is None or time_value < case_times[case][0]):
                case_times[case] = (time_value, time)
    
    sorted_cases = sorted(case_times.items(), key=lambda x: x[1] if x[1] is not None else float('inf'))
    sorted_cases = list(enumerate(sorted_cases, 1))

    return render_template('index.html', times=times, sorted_cases=sorted_cases, pllNames=pllNames)

@app.route('/update_statistics', methods=['GET'])
def update_statistics():
    time_records = TimeRecord.query.all()
    case_times = {}
    pllNames = ["Aa", "Ab", "E", "F", "Ga", "Gb", "Gc", "Gd", "H", "Ja", "Jb", "Na", "Nb", "Ra", "Rb", "T", "Ua", "Ub", "V", "Y", "Z"]

    for record in time_records:
        case = record.caseIndex
        time_value = record.timeValue
        time = record.content
        
        if case not in case_times:
            case_times[case] = (time_value, time)
        else:
            if time_value is not None and (case_times[case][0] is None or time_value < case_times[case][0]):
                case_times[case] = (time_value, time)
    
    sorted_cases = sorted(case_times.items(), key=lambda x: x[1] if x[1] is not None else float('inf'))
    sorted_cases = list(enumerate(sorted_cases, 1))
    return render_template('statistics.html', sorted_cases=sorted_cases,pllNames=pllNames)

@app.route('/update_time', methods=['POST'])
def update_time():
    content = request.form.get('content')
    pll_case = request.form.get('caseIndex')
    centiseconds = request.form.get('timeValue')

    existing_times = TimeRecord.query.all()
    order_index = len(existing_times) + 1 

    new_time = TimeRecord(content=content, id=order_index, caseIndex=pll_case, timeValue=centiseconds)
    db.session.add(new_time)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    try:
        time_to_delete = TimeRecord.query.get_or_404(id)
        db.session.delete(time_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(f"Error deleting time with ID {id}: {e}")
        return 'There was a problem deleting that time'
    
if __name__ == "__main__":
    app.run(debug=True)