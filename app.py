from flask import Flask, render_template,request, redirect,url_for,flash
from flask.wrappers import Request
from flask_mysqldb import MySQL
import mysql.connector

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
    return render_template ('login.html')

@app.route('/register/',  methods=['GET','POST'])
def Register():
    if request.method == 'POST':
        name=request.form['name']
        lastname=request.form['lastname']
        email=request.form['email']
        pasword=request.form['pass']

        cur=db.cursor()
        cur.execute('INSERT INTO client (name, lastname, email, pass) VALUES (%s, %s, %s, %s)',
        (name,lastname,email,pasword))

        db.commit()

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
        name= request.form['name']
        price= request.form['price']
        existence= request.form['existence']
        description= request.form['description']

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
            name= request.form['name']
            price= request.form['price']
            existence= request.form['existence']
            description= request.form['description']   
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



#### no sé que poner




if __name__=='__main__':
    app.run(port=5000,debug=True)