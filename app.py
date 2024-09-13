from flask import Flask, render_template
from dotenv import load_dotenv

# 加载flask环境
load_dotenv(".flaskenv")

app = Flask(__name__)

name = 'gaoxiang'
age = 18
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
numbers = [1, 2,3,4,5 ,6, 7]

@app.route("/")
def index():
  return render_template("index.html", name=name, movies=movies, age=age, numbers=numbers)


@app.route("/test")
def test():
  return '<h1>这个页面是用来做测试的</h1>'