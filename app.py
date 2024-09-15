from flask import Flask, render_template, url_for, request, flash, redirect
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
app.config['SECRET_KEY'] = 'gaoxaing'

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


@app.context_processor
def inject_user():
  user = User.query.first()
  return dict(user=user) 

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.route("/", methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    #拿到表单数据
    title = request.form.get('title')
    year = request.form.get('year')
    #验证数据
    if not title or not year or len(year) > 4 or len(title) > 60:
      flash('Invalid input.')
      return redirect(url_for('index'))
    #保存表单数据
    movie = Movie(title=title, year=year)
    db.session.add(movie)
    db.session.commit()
    flash('Item created')
    return redirect(url_for('index'))
  
  movies = Movie.query.all()
  return render_template("index.html", movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    print(movie.title)
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页

@app.route("/actor")
def actor():
  return render_template("actor.html", actors=actors)

@app.route("/test")
def test():
  return '<h1>这个页面是用来做测试的</h1>'



