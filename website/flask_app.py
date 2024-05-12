# Flask related stuff
from flask import Flask, render_template, request, redirect, url_for, session

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#discord_files
from discord_files.discord_text_files import get_members_text_file, get_guilds_text_file
from discord_files.discord_databases import get_discord_db_path


import settings
from zenora import APIClient
from config import DISCORD_REDIRECT_URL, DISCORD_OAUTH_URL

client = APIClient(settings.DISCORD_API_TOKEN, client_secret=settings.DISCORD_API_SECRET)



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
SqlSession = sessionmaker(bind=engine)
sql_session = SqlSession()


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
app.config["SECRET_KEY"] = "verysecret"

@app.route('/')
def home():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        return render_template("home.html",
                               oauth_url=DISCORD_OAUTH_URL,
                               current_user=current_user,
                               guilds=get_guilds(),
                               filters=sql_session.query(Filter).all())
    return render_template("home.html",
                           guilds=get_guilds(),
                           filters=sql_session.query(Filter).all(),
                           oauth_url=DISCORD_OAUTH_URL)


# @todo - build this app
#         https://www.youtube.com/watch?v=KFt8BpWakMg&t
# discord oauth callback
@app.route("/oauth/callback")
def callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, DISCORD_REDIRECT_URL).access_token
    session['token'] = access_token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route('/members')
def members():
    return render_template("members.html", members=get_members())

@app.route('/add_filter', methods=['POST'])
def add_filter():
    word = request.form.get("word")
    filter = Filter(word=word.lower())
    sql_session.add(filter)
    sql_session.commit()
    return redirect(url_for('home'))


@app.route('/remove_filter', methods=['POST'])
def remove_filter():
    word = request.form.get("word")
    filter = session.query(Filter).filter_by(word=word.lower()).first()
    sql_session.delete(filter)
    sql_session.commit()
    return redirect(url_for('home'))


def run_flask():
    app.run()
