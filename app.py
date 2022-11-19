from queue import Empty
import re, logging
from flask import Flask, render_template, redirect, request, session
from flask.templating import render_template
import random
import sqlite3
 
app = Flask(__name__)
app.secret_key = "KAI"  #loging

@app.route('/MV')
def mv():
    return render_template('MV_times.html')

@app.route('/tukiyomi')
def tukiyomi():
    return render_template('MV_times_tukiyomi.html')
    

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

@app.route('/serch_lylics')
def serch_lylics():
    return render_template('serch_lylics.html')

@app.route("/serch_lylics", methods=["POST"])
def serch_lylics_post():

        # ブラウザから送られてきた歌詞(inputed_lylics)を変数 (lylicsvalue) に入れる
        lylicsvalue_before = request.form.get('inputed_lylics')
        print ("lylicsvalue_before:",lylicsvalue_before)
        #全角スペースを半角スペースに変換
        lylicsvalue = lylicsvalue_before.replace('　',' ')
        #半角?を全角？に変換
        lylicsvalue = lylicsvalue_before.replace('?','？')
        #半角!を全角！に変換
        lylicsvalue = lylicsvalue_before.replace('!','！')
        
        if lylicsvalue =="":
            lylicsvalue = "値を入力してください"
        elif lylicsvalue == " ":
            lylicsvalue = "スペース1つだけでは検索できません"
        elif lylicsvalue == ",":
            lylicsvalue = ", 1つだけでは検索できません"
        elif lylicsvalue == "、":
            lylicsvalue = "、1つだけでは検索できません"
        elif lylicsvalue == "「":
            lylicsvalue = "「1つだけでは検索できません"
        elif lylicsvalue == "」":
            lylicsvalue = "」1つだけでは検索できません"
        elif lylicsvalue == "ー":
            lylicsvalue = "ー1つだけでは検索できません"
        elif lylicsvalue == "（":
            lylicsvalue = "（1つだけでは検索できません"
        elif lylicsvalue == "）":
            lylicsvalue = "）1つだけでは検索できません"
        elif lylicsvalue == "(":
            lylicsvalue = "(1つだけでは検索できません"
        elif lylicsvalue == ")":
            lylicsvalue = ")1つだけでは検索できません"
        else:
            print ("lylicsvalue_after:",lylicsvalue)

        # KP_MusicList.dbに接続
        conn = sqlite3.connect('KP_MusicList.db')
        c = conn.cursor()

        #一致している列をすべてmatch_idsにリストで入れる
        match_idsdup = []
        match_ids = []

        #lylics_displayで検索
        c.execute("SELECT distinct music_name,lylics_by,composition_by,lylics_display FROM product_lylics WHERE lylics_display like ? ", ('%' +lylicsvalue+ '%',)) 
        for row in c.fetchall(): 
            match_idsdup.append({"music_name":row[0],"lylics_by":row[1], "composition_by": row[2], "lylics_display": row[3]})
        #print ("lylics_display:",match_ids)

        #lylicsで検索
        c.execute("SELECT distinct music_name,lylics_by,composition_by,lylics_display FROM product_lylics WHERE lylics like ? ", ('%' +lylicsvalue+ '%',)) 
        for row in c.fetchall(): 
            match_idsdup.append({"music_name":row[0],"lylics_by":row[1], "composition_by": row[2], "lylics_display": row[3]})
        #print ("lylics:",match_ids)

        #lylics_kanaで検索
        c.execute("SELECT distinct music_name,lylics_by,composition_by,lylics_display FROM product_lylics WHERE lylics_kana like ? ", ('%' +lylicsvalue+ '%',)) 
        for row in c.fetchall(): 
            match_idsdup.append({"music_name":row[0],"lylics_by":row[1], "composition_by": row[2], "lylics_display": row[3]})
        #print ("match_idsdup:",match_idsdup)

        def get_unique_list(seq):
            seen = []
            return [x for x in seq if x not in seen and not seen.append(x)]

        match_ids = get_unique_list(match_idsdup)
        print ("match_ids:",match_ids)

        c.close()
        return render_template("/result_lylics.html",html_name=lylicsvalue,html_match_ids=match_ids) 

if __name__ == "__main__":
    app.run()
