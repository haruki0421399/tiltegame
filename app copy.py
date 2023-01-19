from flask import Flask, render_template, request, redirect, url_for, json
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from pathlib import Path
from AVgame import AVgames
import random
import time

give_num = 20
text_path = str(Path(__file__).resolve().parent) + '/wordlist.txt'

deli_hand = []
all_hand = []   
ini_hand= ["セックス", "に", "は", "と", "が", "を", "の", "より", "だけの", "!", "?"]
index_word = []

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))

class Titles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    words = db.Column(db.String)
    postname = db.Column(db.String(10))

# 未実装辞書
# dictionary = AVgames.dic(ini_hand, deli_hand, all_hand) #手札の辞書化

# ini_dic = json.dumps(dictionary[0], indent=4, ensure_ascii=False)
# deli_dic = json.dumps(dictionary[1], indent=4, ensure_ascii=False)
# all_dic = json.dumps(dictionary[2], indent=4, ensure_ascii=False)

# with open('AVgame/static/js/sample.json', 'w') as f:
#     json.dump(dictionary[0], f, indent=4, ensure_ascii=False)


@app.before_first_request
def init():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        Titles.query.delete()
        User.query.delete()
        return render_template('start.html')
    else:
        username = User.query.first().username
        print(username)
        print("wwwwwww")
        eroword = request.form.get('eroword')
        title = Titles(words=eroword)
        db.session.add(title)
        db.session.commit()
        if(Titles.query.count() > 5):
            tmp = Titles.query.first()
            db.session.delete(tmp)
            db.session.commit()
        return redirect('/')

@app.route('/touroku')
def touroku():
    return render_template('touroku.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'GET':
        post = User.query.first()
        return render_template('game.html', post=post)
    else:
        User.query.delete()
        username = request.form.get('username')
        name = User(username=username)
        db.session.add(name)
        db.session.commit()
        return redirect('/game')

@app.route('/<int:id>/playgame', methods=['GET','POST'])
def playgame(id):
    post = User.query.get(id)
    if request.method == 'GET':
        f = open(text_path, 'r')
        words = f.readlines() #ファイルの読み込み
        deli_hand = AVgames.make_hand(words) #手札の生成
        all_hand = AVgames.union(ini_hand, words) #手札の合体
        f.close()
        return render_template('playgame.html', all=all_hand, len=len(all_hand), post=post)
    else:
        return render_template('/playgame')
 
@app.route('/final', methods=['GET', 'POST'])
def final():
    if request.method == 'GET':
        posts = Titles.query.all()
        return render_template('final.html', posts=posts)
    else:
        username = User.query.first().username
        print(username)
        print("wwwwwww")
        eroword = request.form.get('eroword')
        title = Titles(words=eroword, postname=username)
        db.session.add(title)
        db.session.commit()
        if(Titles.query.count() > 5):
            tmp = Titles.query.first()
            db.session.delete(tmp)
            db.session.commit()
        return redirect('/final')

@app.route('/playgame2')
def playgame2():
        f = open(text_path,'r')
        words = f.readlines() #ファイルの読み込み
        deli_hand = AVgames.make_hand(words) #手札の生成
        all_hand = AVgames.union(ini_hand, words) #手札の合体
        return render_template('playgame2.html', all=all_hand, len=len(all_hand))
    
if __name__ == "__main__":
    app.run(debug=True)