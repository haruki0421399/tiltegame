from flask import Flask, render_template, request, redirect, url_for, json
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from pathlib import Path
from AVgame import AVgames
from datetime import datetime
import random
import time
import pytz

give_num = 20
text_path = str(Path(__file__).resolve().parent) + '/wordlist.txt'

deli_hand = []
all_hand = []   
ini_hand= ["セックス", "に", "は", "と", "が", "を", "の", "より", "だけの", "!", "?"]
index_word = []
n_posts = []

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///titlels.db'
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))

class Titles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    words = db.Column(db.String)
    postname = db.Column(db.String(10))
    create_at = db.Column(db.String, nullable=False)

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
    return render_template('start.html')

@app.route('/titlelist', methods=['GET', 'POST'])
def title_list():
    posts = Titles.query.all()
    for i in reversed(posts):
        n_posts.append(i)
    print(n_posts)
    return render_template('titlelist.html', posts=n_posts)

@app.route('/touroku')
def touroku():
    return render_template('touroku.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'GET':
        return render_template('game.html')
    else:
        username = request.form.get('username')
        return render_template('game.html', name=username)

@app.route('/playgame', methods=['GET','POST'])
def playgame():
    if request.method == 'GET':
        f = open(text_path, 'r')
        words = f.readlines() #ファイルの読み込み
        deli_hand = AVgames.make_hand(words) #手札の生成
        all_hand = AVgames.union(ini_hand, words) #手札の合体
        f.close()
        return render_template('playgame.html', all=all_hand, len=len(all_hand), ini=len(ini_hand), deli=len(deli_hand))
    else:
        return render_template('/playgame')
 
@app.route('/<string:name>/final', methods=['GET', 'POST'])
def final(name):
    if request.method == 'GET':
        posts = Titles.query.all()
        posts = posts[-6:-1]
        return render_template('final.html', posts=posts)
    else:
        eroword = request.form.get('eroword')
        tdatetime = datetime.now(pytz.timezone('Asia/Tokyo'))
        tstr = tdatetime.strftime('%Y/%m/%d')
        title = Titles(words=eroword, postname=name, create_at=tstr)
        db.session.add(title)
        db.session.commit()
        return redirect('/' + name + '/final')
    
if __name__ == "__main__":
    app.run(debug=True)