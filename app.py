from flask import Flask, flash, render_template, request, redirect, url_for
import os
import sqlalchemy as db
import sqlite3
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

PRESET_FIRST_LAST = [0, 5]
PRESET_FIRST_LAST_EMAIL = [0, 5, 3]
PRESET_FIRST_LAST_POSITION = [0, 5, 4]

currentDirectory = os.path.dirname(os.path.abspath(__file__))
count = 0

database_path = os.path.join(currentDirectory, 'Orgchart.db')
database_url = f'sqlite:///{database_path}'

engine = db.create_engine(database_url)
metadata = db.MetaData()

Base = declarative_base()

class Members(Base):
    __tablename__ = "Members"
    FirstName = Column(String, primary_key=True)
    PhoneNum = Column(Integer)
    Age = Column(Integer)
    Email = Column(String)
    Position = Column(String)
    LastName = Column(String, primary_key=True)


Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
app.config['SECRET KEY'] = 'August 9, 2024'

@app.route("/")
def main():
    return render_template('Home_page.html')

@app.route("/new", methods =['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        if not request.form['first_name'] or not request.form['last_name'] or not request.form['email'] or not request.form['age']:
            flash('Please enter all the fields', 'error')
        else:
            firstName = request.form['first_name']
            lastName = request.form['last_name']
            email = request.form['email']
            age = request.form['age']
            phoneNum = request.form['phonenum']
            position = request.form['position']
            connection = sqlite3.connect(currentDirectory + "/Orgchart.db")
            cursor = connection.cursor()
            q1 = "INSERT INTO Members(Firstname, Lastname, PhoneNum, Age, Email, Position) VALUES('{fname}', '{lname}', '{phonenum}', '{ag}', '{em}', '{pos}')".format(fname = firstName, lname = lastName, phonenum = phoneNum, ag = age, em = email, pos = position)
            cursor.execute(q1)
            connection.commit()
    return render_template('add_member.html')

@app.route("/delete", methods = ['GET', 'POST'])
def delete_member():
    if request.method == 'POST':
        if not request.form['first_name'] or not request.form['last_name'] or not request.form['email'] or not request.form['age']:
            flash('Please enter all the fields', 'error')
        else:
            firstName = request.form['first_name']
            lastName = request.form['last_name']
            email = request.form['email']
            age = request.form['age']
            phoneNum = request.form['phonenum']
            position = request.form['position']
            connection = sqlite3.connect(currentDirectory + "/Orgchart.db")
            cursor = connection.cursor()
            q1 = "DELETE FROM Members WHERE FirstName = '{fname}' AND LastName = '{lname}' AND PhoneNum = '{pNum}' AND Age = '{ag}' AND Email = '{mail}' AND Position = '{pos}'".format(fname = firstName, lname = lastName, pNum = phoneNum, ag = age, mail = email, pos = position)
            cursor.execute(q1)
            connection.commit()
    return render_template('remove_member.html')

@app.route("/edit", methods = ['GET', 'POST'])
def edit_member():
    if request.method == 'POST':
        if not request.form['selected_first_name'] or not request.form['selected_last_name']:
            flash('Please enter a member to be edited!', 'error')
        else:
            selectedFirstName = request.form['selected_first_name']
            selectedLastName = request.form['selected_last_name']
            firstName = request.form['first_name']
            lastName = request.form['last_name']
            email = request.form['email']
            age = request.form['age']
            phoneNum = request.form['phonenum']
            position = request.form['position']
            connection = sqlite3.connect(currentDirectory + "/Orgchart.db")
            cursor = connection.cursor()
            q1 = "UPDATE Members SET Email = '{em}' WHERE FirstName = '{sfname}' AND LastName = '{slname}'".format(em=email, sfname=selectedFirstName, slname=selectedLastName)
            q2 = "UPDATE Members SET PhoneNum = '{pn}' WHERE FirstName = '{sfname}' AND LastName = '{slname}'".format(pn=phoneNum, sfname=selectedFirstName, slname=selectedLastName)
            q3 = "UPDATE Members SET Position = '{pos}' WHERE FirstName = '{sfname}' AND LastName = '{slname}'".format(pos=position, sfname=selectedFirstName, slname=selectedLastName)
            q4 = "UPDATE Members SET Age = '{ag}' WHERE FirstName = '{sfname}' AND LastName = '{slname}'".format(ag=age, sfname = selectedFirstName, slname=selectedLastName)
            q5 = "UPDATE Members SET FirstName = '{fname}', LastName = '{lname}' WHERE FirstName = '{sfname}' AND LastName = '{slname}'".format(fname=firstName, lname=lastName, sfname=selectedFirstName, slname=selectedLastName)
            if email:
                cursor.execute(q1)
            if phoneNum:
                cursor.execute(q2)
            if position:
                cursor.execute(q3)
            if age:
                cursor.execute(q4)
            if firstName and lastName:
                cursor.execute(q5)
    
            connection.commit()
    return render_template('edit_member.html')

@app.route("/report", methods = ['GET', 'POST'])
def new_report():
    flag = 0
    if request.method == 'POST':
        selected_fields = request.form.getlist('field')  # Get the selected fields from the form
        preset = request.form.get('preset')

        if preset == 'first_last':
            selected_indices = PRESET_FIRST_LAST
            selected_indices = [int(index) for index in selected_indices]
            columns = [Members.__table__.c[i] for i in selected_indices]
            indices = ['First Name', 'Last Name']
            flag = 1
        elif preset == 'first_last_email':
            selected_indices = PRESET_FIRST_LAST_EMAIL 
            selected_indices = [int(index) for index in selected_indices]
            columns = [Members.__table__.c[i] for i in selected_indices]
            indices = ['First Name', 'Last Name', 'Email']
            flag = 1
        elif preset == 'first_last_position':
            selected_indices = PRESET_FIRST_LAST_POSITION
            selected_indices = [int(index) for index in selected_indices]
            columns = [Members.__table__.c[i] for i in selected_indices]
            indices = ['First Name', 'Last Name', 'Position']
            flag = 1
        else:
            columns = [getattr(Members, field) for field in selected_fields]

        # Ensure at least one field is selected
     #   if not selected_fields:
      #     flash('Please select at least one field for the report.', 'error')
       #     return render_template('report.html')

        # Create a list of column objects based on selected_fields

        # Query the database based on the selected fields
        with Session() as session:
            # Use load_only to select specific columns
            members_data = session.query(*columns).all()

        print(members_data)
        if flag == 0:
            return render_template('generated_report.html', members_data=members_data, selected_fields=selected_fields)
        else:
            return render_template('generated_report.html', members_data=members_data, selected_fields=indices)


    return render_template('report.html')


if __name__ == '__main__':
    app.run(debug=True)



    