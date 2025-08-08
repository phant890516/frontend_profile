from flask import Flask , render_template ,request,make_response,session
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime , timedelta
import mysql.connector
import json
import os
import sqlalchemy
import psycopg2
app=Flask(__name__)
app.secret_key="anemori123"
app.permanent_session_lifetime = timedelta(minutes=3)

#session確認し、ログイン状態に応じてindex.html表示------------------------------------------------------------------------------------------------------------------------
@app.route('/',methods=['GET'])
def index():
    if 'ID' in session:
        user = session.get('ID')
    else :
        user = None
    if 'authority' in session:
        authority = session.get('authority')
    else :
        authority = 1   
    return render_template('index.html',user=user,authority=authority)

#Login画面表示----------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login',methods=['GET'])
def login():
    etbl={}
    account={}
      
    return render_template('login.html',etbl=etbl,account=account)

#Login確認--------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login/auth',methods=['POST'])
def login_auth():
    account = request.form
    ecnt = 0
    data = {}
    error = "を入力してください。"
    etbl={}
    stbl={"ID":"ID","password":"パスワード"}
    
    for key,value in account.items():
        if not value:
            ecnt+=1
            etbl[key] = stbl[key] + error
    if ecnt !=0:
        return render_template('login.html',etbl=etbl,account=account)
    
    sql = "SELECT * FROM user WHERE userid = %s;"
    con=connect_db()
    cur=con.cursor(dictionary=True)
    cur.execute(sql,(account['ID'],))
    # 入力した資料がデータベースに存在するかどうかを確認
    userExist = cur.fetchone()
    #ユーザーが存在しない　、　パスワードが間違い 
    if not userExist or userExist['password'] != account['password']:
        etbl['ID'] = "IDまたはパスワードが間違がっています。"
        return render_template('login.html',etbl = etbl,account=account)
    
    session['ID'] = account['ID']
    session['authority'] = userExist['authority']
    return render_template('index.html',user = session.get('ID'),authority = session.get('authority'))
    
#Logout--------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/logout',methods=['GET'])
def logout():
    session.pop('user', None)
    session.pop('authority', None)
    session.clear()
    return render_template('index.html')

#Register-------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/register_user',methods=['GET'])
def register_user():
    account = {}
    etbl ={}
    return render_template('register_user.html',account=account,etbl=etbl)

#Register確認----------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/register_user/complete',methods=['POST'])
def register_user_complete():
    account = request.form
    error = "を入力してください。"
    etbl={}
    stbl={"ID":"ID","password":"パスワード"}
    #入力確認
    ecnt =0
    for key,value in account.items():
        if not value:
            ecnt+=1
            etbl[key] = stbl[key] + error
    if ecnt !=0:
        return render_template('register_user.html',etbl=etbl,account=account)
    
    #同一user確認    
    sql = "SELECT * FROM user WHERE userid = %s;"
    con=connect_db()
    cur=con.cursor(dictionary=True)
    cur.execute(sql,(account['ID'],))
    userSame = cur.fetchone()    
    if userSame:
        etbl['ID'] = "このIDは既に使用されています。"
        return render_template('register_user.html',etbl = etbl,account=account)

    if account['authority']  == "管理者":
        authority = 0
    else:
        authority = 1   
    #DBに登録
    user = (account['ID'],account['password'],authority)
    sql = "INSERT INTO user (userid,password,authority) VALUES(%s,%s,%s)"
    cur.execute(sql,user)  
    con.commit()
    cur.close()
    con.close()

    return render_template('register_user_complete.html',account = account)

#Products表示-----------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/products',methods=['GET'])
def products():   
    #DBに接続し、商品取得
    sql = "SELECT * FROM lunch;"
    con=connect_db()
    cur=con.cursor(dictionary=True)
    cur.execute(sql)
    products=cur.fetchall()
    cur.close()
    con.close()

    return render_template('products.html',products = products ,authority = session.get('authority'))

#Products詳細-----------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/products/<scode>',methods=['GET'])
def product_detail(scode):
    #user確認
    if 'ID' in session:
    #商品資料を取得    
        sql = "SELECT * FROM lunch WHERE scode= %s;"
        con = connect_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql,(scode,))
        result = cur.fetchone()
        cur.close()
        con.close()
        
        return render_template('product_detail.html',result = result)
    
    else:
        return render_template('index.html')

#商品登録画面-----------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/register_product',methods=['GET'])
def register_product_form():
    #権限確認
    authority = session.get('authority')
    if authority != 0:
        return render_template('index.html')
    #更新画面に遷移
    error={}
    return render_template('register_product.html',error=error)
#商品登録--------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/register_product_complete', methods=['POST'])
def register_product_complete():
    #error用
    ecnt =0
    error ={}
    stbl={
    "scode":"商品番号",
    "sname":"商品名",
    "price":"販売価格",
    "detail":"商品説明",
    "img":"ファイル"
    }

    #データ取得
    register = request.form
    if not register['scode'].isdigit():
        error['scode'] = "正整数を入力してください"
        ecnt +=1
    if not register['price'].isdigit():
        error['price'] = "正整数を入力してください"
        ecnt+=1
    
    #空欄確認
    for key, value in register.items():
        if not value:
            error[key] = stbl[key] + "を入力してください"
            ecnt +=1
    
    file = request.files['img']
    if not file:
        ecnt+=1
        error['img'] = stbl['img'] + "が選択されていません"
    if ecnt !=0:
        return render_template('register_product.html',error = error , register = register)
    
    #同一商品確認
    sql = "SELECT * FROM lunch WHERE scode = %s;"
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql,(register['scode'],))
    productExist = cur.fetchone()
    if productExist:
        error['scode'] = "同じ商品が存在する。"
        return render_template('register_product.html',error =error , register = register)
    
    #システム用の画像名生成
    filename = secure_filename(file.filename)
    savedata = datetime.now().strftime("%Y%m%d%H%M%S_")
    filename = savedata + filename
    
    #画像path生成 absolute_path
    current_filepath = os.path.abspath(__file__)
    current_dictionary = os.path.dirname(current_filepath)
    save_path = current_dictionary + "\\static\\img\\" + filename
    
    #画像保存
    image = Image.open(file)
    image.save(save_path,quality = 90)
    image_url = "/static/img/" + filename

    #DBに登録
    data=(register['scode'],register['sname'],int(register['price']),register['detail'],filename)
    sql = "INSERT INTO lunch (scode,sname,price,detail,filename) VALUE (%s,%s,%s,%s,%s)"
    cur.execute(sql,data)
    con.commit()
    cur.close()
    con.close()
    
    return render_template('register_product_complete.html',image_url = image_url ,register = register,authority = session.get('authority'))
#UPDATEページ----------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/update_product/<scode>',methods=['GET'])
def update_product_form(scode):
    #権限確認
    authority = session.get('authority')
    if authority != 0:
        return render_template('index.html')
    error={}
    #商品資料を取得    
    sql = "SELECT * FROM lunch WHERE scode= %s;"
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql,(scode,))
    product = cur.fetchone()
    cur.close()
    con.close()
    
    return render_template('update_product.html',product = product,error=error)

#UPDATE---------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/update_product_complete/<scode>',methods=['POST'])
def update_product_complete(scode):
    #権限確認
    authority = session.get('authority')
    if authority != 0:
        return render_template('index.html')
    
    #資料取得
    fields = ['scode','sname','price','detail']
    product={}
    for field in fields:
        product[field] = request.form.get(field)
        
    file = request.files.get('img')
    
    #error用
    ecnt =0
    error ={}
    stbl={
    "scode":"商品番号",
    "sname":"商品名",
    "price":"販売価格",
    "detail":"商品説明",
    "img":"ファイル"
        }
    
    #空欄確認
    for key, value in product.items():
        if not value:
            error[key] = stbl[key] + "を入力してください"
            ecnt +=1
    
    if not file:
        error['img'] = stbl['img'] + "が選択されていません"
    
    #price int 確認
    if not product['price'].isdigit():
        error['price'] = "正整数を入力してください"
        ecnt+=1

    #画像処理
    image_url =""
    filename = None
    if file and file.filename != "":
        filename = secure_filename(file.filename)
        savedata = datetime.now().strftime("%Y%m%d%H%M%S_")
        filename = savedata + filename   
        #画像path生成 absolute_path
        current_filepath = os.path.abspath(__file__)
        current_dictionary = os.path.dirname(current_filepath)
        save_path = current_dictionary + "\\static\\img\\" + filename
        #画像保存
        image = Image.open(file)
        image.save(save_path,quality = 90)
        image_url = "/static/img/" + filename
        
    #error処理
    if ecnt !=0:
        #元の画像url取得
        sql = "SELECT filename FROM lunch WHERE scode = %s;"
        con = connect_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql, (scode,))
        findImg = cur.fetchone()
        cur.close()
        con.close()
        if findImg:
            product['filename'] = findImg["filename"]

        else:
            product['filename'] = ""
            
        return render_template('update_product.html',error = error , product = product )
        
    #DB更新,順番が一致する必要
    update_fields=[product['sname'],int(product['price']),product['detail']]
    sql = "UPDATE lunch set sname=%s,price=%s,detail=%s"
    if filename:
        sql = sql + ",filename=%s"
        update_fields.append(filename)
    sql = sql + "where scode=%s;"
    update_fields.append(product['scode'])
    
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql,update_fields)
    con.commit()
    cur.close()
    con.close()
    
    #products GET  
    sql = "SELECT * FROM lunch;"
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql)
    products = cur.fetchall()
    cur.close()
    con.close()
    
    # if not image_url :
    #     return render_template('products.html', products = products),201
    
    return render_template('products.html',image_url = image_url , products = products,authority = session.get('authority')),201

#削除ページ---------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/delete_product/<scode>' , methods=['GET'])
def delete_product_confirm(scode):
    #権限確認
    authority = session.get('authority')
    if authority != 0:
        return render_template('index.html')
    
    #商品資料を取得    
    sql = "SELECT * FROM lunch WHERE scode= %s;"
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql,(scode,))
    result = cur.fetchone()
    cur.close()
    con.close()
    
    return render_template('delete_confirm.html',result = result)
#削除実行-----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/delete_product_complete/<scode>' , methods=['POST'])
def  delete_product_complete(scode):
    #権限確認
    authority = session.get('authority')
    if authority != 0:
        return render_template('index.html')
    
    #元の画像url取得
    sql = "SELECT filename FROM lunch WHERE scode = %s;"
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql, (scode,))
    findImg = cur.fetchone()
    cur.close()
    con.close()
    if findImg and findImg['filename']:
        filename = findImg["filename"]
        #画像path生成 absolute_path
        current_filepath = os.path.abspath(__file__)
        current_dictionary = os.path.dirname(current_filepath)
        image_path = current_dictionary + "\\static\\img\\" + filename
        os.remove(image_path)     
   
    # image_path = os.path.join(app.root_path, 'static', 'img', filename)
        
    #商品資料を削除    
    sql = "DELETE FROM lunch WHERE scode= %s;"
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql,(scode,))
    con.commit()
    cur.close()
    con.close()

    
    #DBに接続し、商品取得
    sql = "SELECT * FROM lunch;"
    con=connect_db()
    cur=con.cursor(dictionary=True)
    cur.execute(sql)
    products=cur.fetchall()
    cur.close()
    con.close()
    
    return render_template('products.html',products = products,authority = session.get('authority'))

#DB設定------------------------------------------------------------------------------------------------------------------------------------------------------------------
def connect_db():
    con=mysql.connector.connect(
        host = os.environ.get('AIVEN_DB_HOST'),
        user = os.environ.get('AIVEN_DB_USER'),
        passwd = os.environ.get('AIVEN_DB_PASSWORD'),
        db ='py23db'
    )
    return con

if __name__ == "__main__":
    app.debug = True
    app.run(host='localhost',port='0702')
