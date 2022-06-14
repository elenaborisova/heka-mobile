from datetime import timedelta

from flask import Flask, session, redirect, url_for, render_template, request
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.permanent_session_lifetime = timedelta(minutes=30)

SQLALCHEMY_DATABASE_URI = "postgresql://dpmntntgtgaxfq:80dc3621682ec42eec6ba464eb1226cebf7881dc1d8dad871e11339aa3acd473" \
                          "@ec2-34-242-84-130.eu-west-1.compute.amazonaws.com:5432/d1kqq6n590tnvn"
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
engine = create_engine(SQLALCHEMY_DATABASE_URI)


@app.route('/')
def index():
    return 'Helloooo'


@app.route('/home')
def home():
    return render_template('home.html', patients=fetch_patients_diagnosis())


@app.route('/patient-overview/<patient>')
def patient_overview(patient):
    patients = fetch_patients_diagnosis()
    patient_obj = [p for p in patients if p[0] == patient][0]

    return render_template('patient-overview.html', patient=patient_obj)


@app.route('/task-planning')
def task_planning():
    return render_template('task-planning.html')


@app.route('/task-planning', methods=["POST"])
def handle_task_planning():
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    room = request.form["room"]
    bed = request.form["bed"]
    diagnosis = request.form["diagnosis"]
    risk_factors = request.form["risk-factor"]

    insert_query = f"""
        INSERT INTO patients_diagnosis(first_name, last_name, room, bed, diagnosis, risk_factors)
        VALUES ('{first_name}', '{last_name}', '{room}', '{bed}', '{diagnosis}', '{risk_factors}')
        """

    with engine.connect() as connection:
        connection.execute(insert_query)

        return redirect(url_for("home"))


def fetch_patients_diagnosis():
    select_query = f"""
                SELECT first_name, last_name, room, bed, diagnosis, risk_factors
                FROM patients_diagnosis
                """

    with engine.connect() as connection:
        patients_diagnosis = connection.execute(select_query).fetchall()

    return patients_diagnosis


if __name__ == '__main__':
    app.run()
