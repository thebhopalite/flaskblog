from flask import *
import os
from datetime import date
from flaskext.mysql import MySQL


mysql=MySQL()

app=Flask(__name__)

app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_DB']='codeblog'

mysql.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/blog')
def blog():
    return render_template('blog.html') 

@app.route('/blogpost')
def blogpost():
    return render_template('blog-single.html') 

@app.route('/admin')
def base():
    return render_template('admin.html') 

@app.route('/insertRecord',methods=['POST'])
def insertrecord():
    photo=request.files['photo']
    mycon=mysql.connect()
    mycur=mycon.cursor()
    today=date.today()
    fromdate=today.strftime("%Y-%m-%d")
    status='livepost'
    data=[request.form['postname'],request.form['posttitle'],photo.filename,request.form['postcontent'],fromdate,status]
    mycur.execute("INSERT INTO `codingblog`(`postname`, `posttitle`,`postimage`,`postcontent`,`dateandtime`,`status`)VALUES(%s,%s,%s,%s,%s,%s)",data)
    photo.save(os.path.join('static/upload',photo.filename))
    
    return "Done"    
    
@app.route('/managepost',methods=['GET'])
def managepost():
    mycon=mysql.connect()
    mycur=mycon.cursor()
    mycur.execute("select * from codingblog where status='livepost'")
    data=mycur.fetchall()
    return render_template('managepost.html',data=data)
  
@app.route('/deletepost',methods=['GET'])
def deletepost():
    uid=request.args.get('uid')
    mycon=mysql.connect()
    mycur=mycon.cursor()
    mycur.execute("update codingblog set status='deleted' where uid=%s",uid)
    return redirect(url_for('managepost'))

@app.route('/removedpost',methods=['GET'])
def removedpost():
    mycon=mysql.connect()
    mycur=mycon.cursor()
    mycur.execute("select * from codingblog where status='deleted'")
    data=mycur.fetchall()
    return render_template('deletedpost.html',data=data)

@app.route('/restorepost',methods=['GET'])
def restorepost():
    uid=request.args.get('uid')
    mycon=mysql.connect()
    mycur=mycon.cursor()
    mycur.execute("update codingblog set status='livepost' where uid=%s",uid)
    return redirect(url_for('managepost'))
   




app.run(debug=True,port=565323)    