# Flask related stuff
from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#discord_files
from discord_files.discord_text_files import get_members_text_file, get_guilds_text_file
from discord_files.discord_databases import get_discord_db_path

# SQLA
engine = create_engine(f'sqlite:///{get_discord_db_path()}')
Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True, unique=True)

class Filter(Base):
    __tablename__ = 'filter'
    word = Column(String, primary_key=True, unique=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# @todo
# FLASK RELATED STUFF
def get_guilds() -> list:
    file = open(get_guilds_text_file(), 'r')
    data = file.readlines()
    file.close()
    data = [i.replace('\n', '') for i in data]
    data = [i.split(":") for i in data]
    guilds = data
    return guilds


def get_members() -> list:
    with open(get_members_text_file(), 'r') as file:
        data = file.readlines()

    data = [i.replace('\n', '') for i in data]
    data = [i.split(":") for i in data]
    players = data

    return players



app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", guilds=get_guilds(), filters=session.query(Filter).all())


@app.route('/members')
def members():
    return render_template("members.html", members=get_members())


@app.route('/add_filter', methods=['POST'])
def add_filter():
    word = request.form.get("word")
    filter = Filter(word=word.lower())
    session.add(filter)
    session.commit()
    return redirect(url_for('home'))


@app.route('/remove_filter', methods=['POST'])
def remove_filter():
    word = request.form.get("word")
    filter = session.query(Filter).filter_by(word=word.lower()).first()
    session.delete(filter)
    session.commit()
    return redirect(url_for('home'))


def run_flask():
    app.run()
