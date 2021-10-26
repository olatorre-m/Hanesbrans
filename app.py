from flask import Flask, render_template,request, redirect,url_for,flash
from flask.wrappers import Request
from flask_mysqldb import MySQL
from markupsafe import escape 
import mysql.connector
import hashlib
from db import seleccion, accion

app=Flask(__name__)

app.secret_key="mysecretkey"

db = mysql.connector.connect(
   host="localhost",
   user="root",
   passwd="crakwz503",
   database='hanes'
)
mysql=MySQL(app)

@app.route('/')
@app.route('/index/')
def Index():
    cur = db.cursor()
    cur.execute('SELECT * FROM product')
    data=cur.fetchall()
    return render_template('index.html', products=data)

@app.route('/login/', methods=['GET', 'POST'])
def Login():

    '''
    email=request.form['email']
    encoder=str(request.form['pass']).encode()
    formpasword=hashlib.sha256(encoder).hexdigest()
    cur=db.cursor()
    temp=cur.execute('SELECT FROM CLIENT (email) VALUES (%s)', email)
    print(temp)

    if formpasword==password:
        pass
        '''

    return render_template ('login.html')

@app.route('/register/',  methods=['GET','POST'])
def Register():
    
    if request.method == 'POST':
        name=escape(request.form['name'])
        lastname=escape(request.form['lastname'])
        email=escape(request.form['email'])

        swerror=False
        if name==None or len(name)==0:
            flash('ERROR: Debe suministrar un nombre')
            swerror = True
        if lastname==None or len(lastname)==0:
            flash('ERROR: Debe suministrar un apellido')
            swerror = True
        if email==None or len(email)==0:
            flash('ERROR: Debe suministrar un email')
            swerror = True
        if not swerror :
            
            encoder=str(escape(request.form['pass'])).encode()
            pasword=hashlib.sha256(encoder).hexdigest()
            
            cur=db.cursor()
            cur.execute('INSERT INTO client (name, lastname, email, pass) VALUES (%s, %s, %s, %s)',
            (name,lastname,email,pasword))

            db.commit()

        else:
            flash('INFO: Los datos no fueron almacenados')

    return render_template ('registro.html')
    

@app.route('/admin/', methods=['GET', 'POST'])
def Admin():
    return render_template ('admin.html')

@app.route('/adminproduct/', methods=['GET', 'POST'])
def Admin_product():

    cur = db.cursor()
    cur.execute('SELECT * FROM product')
    data=cur.fetchall()
    return render_template('adminproducto.html', products=data)

@app.route('/addproduct/', methods=['GET', 'POST'])
def Add_product():
    if  request.method == 'POST':
        name= escape(request.form['name'])
        price= escape(request.form['price'])
        existence= escape(request.form['existence'])
        description= escape(request.form['description'])

        cur = db.cursor()
        cur.execute('INSERT INTO product (name, price, existence, description) VALUES(%s, %s, %s,%s)',
        (name,price,existence,description))
        db.commit()
        flash('Producto agregado correctamente')


    return redirect(url_for('Admin_product'))


@app.route('/edit/<string:id>')
def get_product(id):

    cur = db.cursor()
    cur.execute(f'SELECT * FROM product WHERE id={id}' )
    data= cur.fetchall()
    return render_template('editproduc.html', product = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_product(id):
    if request.method=='POST':
            name= escape(request.form['name'])
            price= escape(request.form['price'])
            existence= escape(request.form['existence'])
            description= escape(request.form['description'])   
            cur = db.cursor()
            cur.execute("""
            UPDATE product
            SET name =%s,
                price = %s,
                existence= %s,
                description= %s
            WHERE id = %s
            """, (name,price,existence,description,id))
            db.commit()
            flash('Prodcuto actualizado correctamente')
    return redirect(url_for('Admin_product'))


@app.route('/delete/<string:id>')
def delete_product(id):
    cur = db.cursor()
    cur.execute('DELETE FROM product WHERE id = {0}'. format(id))
    db.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('Admin_product'))


@app.route('/adminuser/', methods=['GET', 'POST'])
def Admin_user():

    cur = db.cursor()
    cur.execute('SELECT * FROM client')
    data=cur.fetchall()
    return render_template('adminuser.html', users=data)


@app.route('/deleteuser/<string:id>')
def delete_user(id):
    cur = db.cursor()
    cur.execute('DELETE FROM client WHERE id = {0}'. format(id))
    db.commit()
    flash('Usuario eliminado correctamente')
    return redirect(url_for('Admin_user'))


if __name__=='__main__':
    app.run(port=5000,debug=True)