from queue import Empty
import re, logging
from flask import Flask, render_template, redirect, request, session
from flask.templating import render_template
import random
import sqlite3

app = Flask(__name__)
app.secret_key = "KAI"  #loging

@app.route('/')
def top():
    return render_template('index.html')

@app.route('/album')
def album():
    return render_template('album.html')

@app.route('/dvd')
def dvd():
    return render_template('dvd.html')

@app.route('/serch_music')
def serch_music():
    return render_template('serch_music.html')

@app.route("/serch_music", methods=["POST"])
def serch_music_post():

        # ブラウザから送られてきた曲名(musicserch)を変数 (musicname) に入れる
        musicname = request.form.get("musicserch")
        print (musicname)
        # KP_MusicList.dbに接続
        conn = sqlite3.connect('KP_MusicList.db')
        c = conn.cursor()

        #一致している列をすべてmatch_idsにリストで入れる
        match_ids = []
        c.execute("SELECT music_name,media_category,media_no,media_name,media_ver FROM product WHERE music_name like ? ", ('%' +musicname+ '%',)) 
        for row in c.fetchall(): 
            match_ids.append({"music_name":row[0],"media_category":row[1], "media_no": row[2],"media_name": row[3],"media_ver": row[4]})
        c.close()


        if match_ids is Empty:
            serch_ER = "指定したキーワードに合致する検索結果がありません"
#            # 検索失敗すると、検索画面に戻す
            return render_template("/result_ng.html",html_name=musicname,html_serch_ER=serch_ER)
        else:
            return render_template("/result.html",html_name=musicname,html_match_ids=match_ids)  

if __name__ == "__main__":
    app.run()