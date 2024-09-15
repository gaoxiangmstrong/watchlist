from flask import Flask, render_template, url_for
from dotenv import load_dotenv
from faker import Faker
from flask_sqlalchemy import SQLAlchemy
import os
import click

fake = Faker()
# 加载flask环境
load_dotenv(".flaskenv")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')

db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20))


class Movie(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(60))
  year = db.Column(db.Integer)


# 生成虚拟数据
@app.cli.command()
def forge():
  db.create_all()
  name = 'gaoxiang'
  movies = [
      {'title': 'My Neighbor Totoro', 'year': '1988'},
      {'title': 'Dead Poets Society', 'year': '1989'},
      {'title': 'A Perfect World', 'year': '1993'},
      {'title': 'Leon', 'year': '1994'},
      {'title': 'Mahjong', 'year': '1996'},
      {'title': 'Swallowtail Butterfly', 'year': '1996'},
      {'title': 'King of Comedy', 'year': '1999'},
      {'title': 'Devils on the Doorstep', 'year': '1999'},
      {'title': 'WALL-E', 'year': '2008'},
      {'title': 'The Pork of Music', 'year': '2012'},
  ]
  user = User(name=name)
  db.session.add(user)
  for m in movies:
    movie = Movie(title=m['title'], year=m['year'])
    db.session.add(movie)
  db.session.commit()
  click.echo('Done.')


actors = [{"name":fake.name(), "address": fake.address()} for _ in range(10)]

  
numbers = [1, 2,3,4,5 ,6, 7]

@app.route("/")
def index():
  user = User.query.first()
  movies = Movie.query.all()

  return render_template("index.html",user=user, movies=movies)

@app.route("/actor")
def actor():
  return render_template("actor.html", actors=actors)

@app.route("/test")
def test():
  return '<h1>这个页面是用来做测试的</h1>'