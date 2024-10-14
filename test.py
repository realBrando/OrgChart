from flask import Flask, flash, render_template, request
import os
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

currentDirectory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(currentDirectory, 'Orgchart.db')
database_url = f'sqlite:///{database_path}'

engine = db.create_engine(database_url)
metadata = db.MetaData()

Base = declarative_base()

class members(Base):
    __tablename__ = "Members"
    FirstName = Column(String, primary_key=True)
    PhoneNum = Column(Integer)
    Age = Column(Integer)
    Email = Column(String)
    Position = Column(String)
    LastName = Column(String, primary_key=True)


Session = sessionmaker(bind=engine)
session = Session()

# Query all members from the Members table
all_members = session.query(members).all()

# Print the results
for member in all_members:
    print(f"{member.FirstName} {member.LastName}, {member.Position}, {member.Age} years old, Phone: {member.PhoneNum}, Email: {member.Email}")



