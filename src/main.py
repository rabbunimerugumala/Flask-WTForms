import traceback
from flask import Flask, render_template, request
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from flask_wtf import file

from schemas import RegisterPersonalInformation, EditPersonalInformation

# ! create flask app.
app = Flask(__name__)

# ! Giving the path to the data base.
db_path = Path().cwd() / "src/db/database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + str(db_path)
db = SQLAlchemy(app)


# from models import PersonalDetails
class PersonalDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    mobile_no = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    bio = db.Column(db.String(500))
    password = db.Column(db.String(100))
    confirm_password = db.Column(db.String(100))


@app.get('/')
def index():
    return render_template("index.html", page_heading="DashBoard")


@app.route('/add_personal_details', methods=['GET', 'POST'])
def add_personal_details():
    form = RegisterPersonalInformation(request.form)

    if request.method == 'POST' and form.validate():
        try:
            first_name: str = request.form.get('first_name', '').strip()
            last_name: str = request.form.get('last_name', '').strip()
            date_of_birth: datetime = datetime.strptime(request.form.get('date_of_birth').strip(), '%Y-%m-%d')
            gender: str = request.form.get('gender', '').strip()
            mobile_no: str = request.form.get('mobile_no', '').strip()
            email: str = request.form.get('email', '').strip()
            bio: str = request.form.get('bio', '').strip()
            password: str = request.form.get('password', '').strip()
            confirm_password: str = request.form.get('confirm_password', '').strip()
            # image: file= request.form.get('image')
            personal_details = PersonalDetails(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth,
                                                gender=gender, mobile_no=mobile_no, email=email, bio=bio,
                                                password=password, confirm_password=confirm_password)
            db.session.add(personal_details)
            db.session.commit()

            return render_template('add_personal_details.html', page_heading="Add a New Details", form=form,
                                    status="success")
        except Exception as e:
            traceback.print_exc()
            return render_template('add_personal_details.html', page_heading="Add a New Details", form=form,
                                    status="error")

    return render_template('add_personal_details.html', page_heading="Add a New Details", form=form)


@app.get('/get_details/<int:student_id>')
def get_details(student_id):
    personal_details = PersonalDetails.query.filter_by(id=student_id).first()
    return render_template('get_details.html', page_heading='View Personal Details', details=personal_details)


@app.get("/view_details")
def view_details():
    try:
        # ! querying all the students
        personal_details = PersonalDetails.query.all()
        # table headings
        headings = ('ID', 'First Name', 'Last Name', 'View', 'Action')
        # ! rendering the template
        return render_template("view_details.html", page_heading='Details', headings=headings, details=personal_details)
    except Exception as e:
        traceback.print_exc()
        print(f'*** Error: Something went wrong while querying the details from DB: {str(e)} ***')


@app.route('/edit_student/<int:student_id>', methods=('GET', 'POST'))
def edit_student(student_id):
    details = PersonalDetails.query.filter(PersonalDetails.id == student_id).first()
    form = EditPersonalInformation(request.form)

    if request.method == 'POST' and form.validate():
        try:
            # updating the existing student details
            details.first_name = request.form.get('first_name', '')
            details.last_name = request.form.get('last_name', '')
            details.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d')
            details.gender = request.form.get('gender')
            details.mobile_no = request.form.get('mobile_no')
            details.email = request.form.get('email')
            details.bio = request.form.get('bio')

            # commiting the changes
            db.session.commit()

            # redirect to students page
            return render_template('edit_details.html', page_heading='Edit Details', detail=details, status="success",
                                   form=form)
        except Exception as e:
            traceback.print_exc()
            return render_template('edit_details.html', page_heading='Edit Details', detail=details, status="error",
                                   form=form)

    return render_template('edit_details.html', page_heading='Edit Details', detail=details, form=form)
