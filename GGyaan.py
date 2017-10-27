
import os
from flaskext.mysql import MySQL
from flask import Flask,request,render_template,flash,redirect,session
from wtforms import Form, BooleanField, StringField, PasswordField, validators

mysql = MySQL()

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='development key'
))


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234567890'
app.config['MYSQL_DATABASE_DB'] = 'dbms'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
mysql.init_app(app)

def companyinit():
	session['company']=list()

	conn = mysql.connect()
	cursor = conn.cursor()
	
	cursor.execute('''SELECT * from COMPANY''')
	a = cursor.fetchall()
	if a is not None:
		for i in a:
			session['company'].append(i)
			
	else:
		pass
	cursor.close()
	conn.close()

@app.context_processor
def inject_user():
    return dict(session=session)


@app.route('/', methods = ['GET','POST'])
@app.route('/home', methods = ['GET','POST'])
def home():
	if 'username' in session:
		companyinit()
		return render_template('home.html',flag=True)
	return render_template('index.html', flag=False)

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
			session['username']=request.form['rno']
			session['type']='student'
			companyinit()

			conn.commit()
			cursor.close()
			conn.close()
			return redirect("/home")
			#return render_template('home.html')

		except:
			sucess = False;
		cursor.close()
		conn.close()
		flash("Registration status:"+str(sucess));
		return render_template('index.html',flag=sucess)

@app.route('/logout', methods = ['GET','POST'])
def logout():
		session.pop('username',None)
		session.pop('type',None)
		session.pop('fname',None)
		return render_template('index.html',flag=False)

@app.route('/authenticate', methods = ['GET','POST'])
def authenticate():
	
	conn = mysql.connect()
	cursor = conn.cursor();

	rno = "\'"+str(request.form['rno'])+"\'"
	password = "\'"+str(request.form['passw'])+"\'"

	cursor.execute('''SELECT fname from USERBASE WHERE rno='''+rno+''' AND password=  '''+ password)
	a = cursor.fetchone()
	if a is not None:
		for i in a:
			session['username']=request.form['rno']
			session['type']='student'
			session['fname']=i
			companyinit()
			return redirect("/home")
			
	else:
		cursor.execute('''SELECT * from IC WHERE username='''+rno+''' AND passwd=  '''+ password)
		a = cursor.fetchone()
		if a is not None:
				a = a[0]
				session['username']=request.form['rno']
				cursor.execute('''SELECT fname from USERBASE WHERE rno='''+rno)
				fname = cursor.fetchone()
				session['fname'] = fname[0]
				session['type']='ic'
				companyinit()
				return redirect("/home")	
			
		else:
			return "FAILED!"

	
	
	
@app.route('/profile', methods = ['GET','POST'])
def profile():
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT * from STUDENT WHERE rno=\'"+session['username']+"\';")
	record_tuple = cursor.fetchone()
	record = {}
	#or record['fname']==None or record['fname']=='NULL':
	cursor.execute("SELECT * from USERBASE WHERE rno=\'"+session['username']+"\';")
	user = cursor.fetchone()
		
	record['fname'] = user[0]
	record['lname'] = user[1]
	record['rno'] = session['username']
	if record_tuple is not None:
		record['address']=record_tuple[1]
		record['cgpa'] = record_tuple[2]
		record['resume'] = record_tuple[3]
		record['testexp'] = record_tuple[4]
	else:
		record['address']=None
		record['cgpa'] =None
		record['resume'] =None
		record['testexp'] =None
	

	cursor.close()
	conn.close()
	return render_template('profile.html',prefill=record)
		

@app.route('/profilefill',methods = ['GET','POST'])
def profilefill():
	print(request)
	print(request.method)
	if request.method == 'POST': #and form.validate()
		conn = mysql.connect()
		cursor = conn.cursor()		
		
		addressLine1 = str(request.form['address_line1']);
		addressLine2 = str(request.form['address_line2']);
		addressLine3 = str(request.form['address_line3']);
		addressLine4 = str(request.form['address_line4']);
		
		address = addressLine1 + " " + addressLine2 + " " + addressLine3 + " " + addressLine4;
		address = "\'"+address+"\'";
		cgpa = str(request.form['cgpa']);
		resume = "\'"+str(request.form['resume'])+"\'";
		#testexp = "\'"+str(request.form['testexp'])+"\'";
		
		
		if(address==''):
			address='NULL'
		if(cgpa==''):
			cgpa='NULL'
		if(resume==''):
			resume='NULL'
		testexp = 'NULL'
		
		
		
		cursor.execute('''SELECT rno from STUDENT WHERE rno='''+"\'"+session['username']+"\'")
		a = cursor.fetchone()
		
		try:	
			if a is not None:
				cursor.execute('''DELETE FROM STUDENT WHERE rno='''+"\'"+session['username']+"\'")

			
			cursor.execute(''' INSERT INTO STUDENT values( '''+"\'"+session['username']+"\'"+','+address+','+cgpa+','+resume	+','+testexp+''')''')
			conn.commit()
			
		except:
			pass		
		cursor.close()
		conn.close()
		return redirect("/home")
	else:
		return "FAIL"
		#return render_template('home.html')	
		
@app.route('/company', methods = ['GET','POST'])
def company():
	return render_template('company.html')

@app.route('/mobilelogin',methods=['GET','POST'])
def mobilelogin():
	print(request.values['rno'])
	unname = request.values['rno']
	pword = request.values['password']



	print(type(request.values))
	return "sucess"			
		
@app.route('/companyfill',methods = ['GET','POST'])
def companyfill():
	if request.method == 'POST': #and form.validate()
		conn = mysql.connect()
		cursor = conn.cursor()		
		
		
		cname = "\'"+str(request.form['cname'])+"\'";
		intake = str(request.form['intake']);
		stipend = str(request.form['stipend']);
		
		benefit = "\'"+str(request.form['benefit'])+"\'";
		cdate = "\'"+str(request.form['cdate'])+"\'";
		ctime = "\'"+str(request.form['ctime'])+"\'";
		
		if(intake==''):
			intake='NULL'
		if(stipend==''):
			stipend='NULL'
		if(benefit==''):
			benefit='NULL'
		if(cdate==''):
			cdate='NULL'
		if(ctime==''):
			ctime='NULL'
			
		cursor.execute('''SELECT cname from COMPANY WHERE cname='''+cname)
		a = cursor.fetchone()

		try:
			
			if a is not None:
				cursor.execute('''DELETE FROM COMPANY WHERE cname='''+cname)

			
			cursor.execute(''' INSERT INTO COMPANY values( '''+cname+','+intake+','+stipend+','+benefit+','+cdate+','+ctime+','+"\'"+session['username']+"\'"''')''')
			conn.commit()
		except:
			pass		
	
		
		cursor.close()
		conn.close()
		return redirect('/home')
	
	
	

if __name__ == "__main__":
	#app.run(host="0.0.0.0",debug=True)
	app.run(debug=True)
