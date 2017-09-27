import os
from flaskext.mysql import MySQL

from flask import Flask,request,render_template, flash

from wtforms import Form, BooleanField, StringField, PasswordField, validators

mysql = MySQL()

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'

))

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234567890'
app.config['MYSQL_DATABASE_DB'] = 'dbms'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

mysql.init_app(app)

@app.route('/')
@app.route('/login')
def login():
	return render_template('index.html', flag=True)

@app.route('/register',methods = ['GET','POST'])
def register():
	if request.method == 'POST': #and form.validate()
		conn = mysql.connect()
		cursor = conn.cursor()
		
		fname = "\'"+str(request.form['fname'])+"\'";
		lname = "\'"+str(request.form['lname'])+"\'";
		rno = "\'"+str(request.form['rno'])+"\'";
		email = "\'"+str(request.form['email'])+"\'";
		password = "\'"+str(request.form['password'])+"\'";
		sucess = True;
		try:
			cursor.execute(''' INSERT INTO USERBASE values( '''+fname+','+lname+','+rno	+','+email+','+password+''')''')
			conn.commit()
		except:
			sucess = False;
		cursor.close()
		conn.close()
		flash("Registration status:"+str(sucess));
		return render_template('index.html',flag=sucess)



@app.route('/authenticate', methods = ['GET','POST'])
def authenticate():
	conn = mysql.connect()
	cursor = conn.cursor();

	email = "\'"+str(request.form['email'])+"\'"
	password = "\'"+str(request.form['passw'])+"\'"

	cursor.execute('''SELECT fname from USERBASE WHERE email='''+email+''' AND password=  '''+ password)
	a = cursor.fetchone()
	if a is not None:
		for i in a:
			return i+" logged in!"
	else:
		return "FAILED!"

	return str(a);

if __name__ == "__main__":
	app.run()

