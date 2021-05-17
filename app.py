from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskdb'

db_obj = MySQL(app)

@app.route('/')#Read
def index():
    connect = db_obj.connection.cursor()
    connect.execute("SELECT  * FROM employee")
    data = connect.fetchall()
    connect.close()

    return render_template('index.html', data=data )

@app.route('/addemployee', methods = ['GET','POST']) #Create
def addemployee():
    
    if request.method == "POST":
        ename = request.form['name']
        designation = request.form['designation']
        phoneno = request.form['phoneno']
        
        connect = db_obj.connection.cursor()
        connect.execute("INSERT INTO employee (ename, designation, phoneno) VALUES (%s, %s, %s)", (ename, designation, phoneno))
        db_obj.connection.commit()

        return redirect(url_for('index'))
     
    else:
     	return render_template('addemployee.html')

@app.route('/update/<int:employeeid>', methods = ['GET','POST'])#Update
def update(employeeid):
    print(employeeid)
    if request.method == "POST":
        ename = request.form['ename']
        designation = request.form['designation']
        phoneno = request.form['phoneno']
        connect = db_obj.connection.cursor()
        connect.execute("""
               UPDATE employee
               SET ename=%s, designation=%s, phoneno=%s
               WHERE employeeid=%s
            """, (ename, designation, phoneno, employeeid))
        db_obj.connection.commit()
        return redirect(url_for('index'))
    else:
        connect = db_obj.connection.cursor()
        connect.execute("SELECT  * FROM employee where employeeid=%s", (employeeid,))
        data = connect.fetchall()
        connect.close()
        return render_template('update.html', employeeid=employeeid, data=data)

@app.route('/deleteemployee/<int:employeeid>')#Delete
def deleteemployee(employeeid):
    if employeeid:
        connect = db_obj.connection.cursor()
        connect.execute("DELETE FROM employee WHERE employeeid=%s",(employeeid,))
        db_obj.connection.commit()

        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
