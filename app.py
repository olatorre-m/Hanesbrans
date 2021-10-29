import re
from flask import Flask, render_template,request, redirect, session, sessions,url_for,flash,send_from_directory
from flask.templating import render_template_string
from flask.wrappers import Request
from flask_mysqldb import MySQL
from markupsafe import escape 
import mysql.connector
import hashlib
import bcrypt
from werkzeug.security import check_password_hash,generate_password_hash
import os
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
semilla=bcrypt.gensalt()

@app.route('/')
@app.route('/index/')
def Index():
    cur = db.cursor()
    cur.execute('SELECT * FROM product')
    data=cur.fetchall()
   
    # return redirect(url_for('Index',products=data))
    
    
    return render_template('index.html', products=data)
   

@app.route('/register/',  methods=['GET', 'POST'])
def Register():
    
        if request.method == 'POST':
            name=request.form['name']
            lastname=request.form['lastname']
            email=request.form['email']
            password=request.form['pass']
            password_encode=password.encode("utf-8")
            password_encriptado=bcrypt.hashpw(password_encode,semilla)
            # swerror=False
            # if name==None or len(name)==0:
            #     flash('ERROR: Debe suministrar un nombre')
            #     swerror = True
            # if lastname==None or len(lastname)==0:
            #     flash('ERROR: Debe suministrar un apellido')
            #     swerror = True
            # if email==None or len(email)==0:
            #     flash('ERROR: Debe suministrar un email')
            #     swerror = True
            # if not swerror :
                         
            

            cur=db.cursor()
            cur.execute('INSERT INTO client (name, lastname, email, pass) VALUES (%s, %s, %s, %s)',
            (name,lastname,email,password_encriptado))

            db.commit()
            #registrar sesion
            session['name']=name
            session['email']=email
            
            return redirect(url_for('Login'))
            

        else:
            flash('Registro exitoso !!!')

        return render_template('registro.html')
    
@app.route('/login/', methods=['GET', 'POST'])
def Login():
     if request.method == 'POST':
        
    #     if 'name' in session:
    #         return render_template ('admin.html')
    #     else:
    #         return render_template ('login.html')
    # else:           
        email=request.form['email']
        password=request.form['password']
        password_encode=password.encode("utf-8")
            
        cur=db.cursor()
        # cur.execute('SELECT name, email, pass FROM client WHERE email = %s',
        # (email))
        sQuery="SELECT name, email, pass FROM client WHERE email = %s"
        cur.execute(sQuery,[email])

        usuario=cur.fetchone()
        cur.close

        if usuario !=None:
            password_encriptado_encode=usuario[2].encode()

                #verificar password 
            if (bcrypt.checkpw(password_encode,password_encriptado_encode)):

                    #registrar sesion
                session['name']=usuario[0]

                if email == 'deividj.54@gmail.com':
                    session['email']=usuario[1]
                
                return redirect(url_for('Index'))
            else:

                flash('La contraseña es incorrecta')
                return render_template ('login.html')
        else:

            flash('El correo ingresado no existe')
     return render_template('login.html')





    



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

@app.route('/comentario/',methods=['GET', 'POST'])
def Comentario():
     
    
 return render_template('descripcion.html')


@app.route('/salir/')
def Salir():

    session.clear()
    return redirect(url_for('Index'))

@app.route('/recuperar/', methods=['GET', 'POST'] )
def Recuperar():
    if request.method=='POST':
        email=request.form['email']
        emailcon=request.form['emailcon']

        if email==emailcon:
            flash('Se envio un enlace a tu correo:')
            return redirect(url_for('Login'))
        else:
            flash('No hay coincidencia en los correos')
    
    return render_template('recuperar.html')

if __name__=='__main__':
    app.run(port=5000,debug=True)