from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyectoav'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT count(*) FROM contacts')
    data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT count(*) FROM factorys')
    data2 = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT count(*) FROM products')
    data3 = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('select c.ID, c.fullname, count(f.ID_contacts) as `Cantidad de fabricas` from factorys f, contacts c where c.ID = f.ID_contacts group by f.ID_contacts')
    data4 = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts=data[0], factorys=data2[0], countContactFactorys=data4, products = data3)

@app.route('/view_factorysContact/<id>')
def factorysContact(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT f.ID, f.name, f.description, f.`type` FROM factorys f WHERE f.ID_contacts = %s', [id])
    data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT c.id, c.fullname FROM contacts c WHERE c.ID = %s', [id])
    data2 = cur.fetchall()
    cur.close()
    return render_template('view_factorysContact.html', factorysContacts=data, fullname=data2)

@app.route('/edit_factory/<id>', methods=['POST', 'GET'])
def get_factory(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM factorys WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    return render_template('edit_factory.html', factory=data[0])

@app.route('/updateFactory/<id>', methods=['POST'])
def update_factory(id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        tipo = request.form['type']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE factorys
            SET name = %s,
                description = %s,
                type = %s
            WHERE id = %s
        """, (name, description, tipo, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete_factory/<id>', methods=['POST', 'GET'])
def delete_factory(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM factorys WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

@app.route('/view_totalFactory')
def getTotalFactory():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM factorys')
    data = cur.fetchall()
    cur.close()

    return render_template('view_totalFactory.html', Factorys=data)

@app.route('/add_factory')
def add_factory():
    cur = mysql.connection.cursor()
    cur.execute('SELECT c.ID, c.fullname FROM contacts c')
    data = cur.fetchall()
    cur.close()
    return render_template('add_factory.html', contacts=data)

@app.route('/CreateFactory', methods=['GET', 'POST'])
def CreateFactory():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        tipo = request.form['type']
        id_contact = request.form.get('id_contact')        

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO factorys (name, description, type, ID_contacts) VALUES (%s,%s,%s,%s)",
                    (name, description, tipo, id_contact))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/add_factoryContact/<id>')
def add_factoryContact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT c.ID, c.fullname FROM contacts c WHERE c.id = %s', [id])
    data = cur.fetchall()
    cur.close()
    return render_template('add_factoryContact.html', contacts=data)

@app.route('/CreateFactoryContact', methods=['GET', 'POST'])
def CreateFactoryContact():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        tipo = request.form['type']
        id_contact = request.form.get('id_contact')        

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO factorys (name, description, type, ID_contacts) VALUES (%s,%s,%s,%s)",
                    (name, description, tipo, id_contact))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/add_contact')
def add_contact():
    flash('Contact Added successfully')
    return render_template('add_contact.html')

@app.route('/CreateContact', methods=['GET', 'POST'])
def CreateContact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']        

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)",
                    (fullname, phone, email))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/view_contacts')
def view_contacts():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()

    flash('Contact Added successfully')
    return render_template('view_contacts.html', contacts = data)

@app.route('/edit_contact/<id>', methods=['POST', 'GET'])
def get_contacts(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    return render_template('edit_contact.html', contact=data[0])

@app.route('/updateContact/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                phone = %s,
                email = %s
            WHERE id = %s
        """, (fullname, phone, email, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete_contact/<id>', methods=['POST', 'GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

@app.route('/add_product')
def add_product():
    cur = mysql.connection.cursor()
    cur.execute('SELECT f.ID, f.name FROM factorys f')
    data = cur.fetchall()
    cur.close() 
    return render_template('add_product.html', factorys=data)

@app.route('/CreateProduct', methods=['GET', 'POST'])
def CreateProduct():
    if request.method == 'POST':
        name = request.form['name']
        stock = request.form['stock']
        price = request.form['price']  
        description = request.form['description']   
        id_factory = request.form.get('id_factorys') 
            

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (name, stock, price,description) VALUES (%s,%s,%s,%s)",
                    (name, stock, price,description))
        flash('Contact Updated Successfully')
        mysql.connection.commit()


        cur = mysql.connection.cursor()
        cur.execute('select p.id  from products p order by p.ID desc limit 1')
        id_product = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('select p.name  from products p order by p.ID desc limit 1')
        name_product = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO factorys_products VALUES (%s,%s,%s)",
                    (id_factory, id_product,name_product))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/add_productFactory/<id>')
def add_productFactory(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT f.ID, f.name FROM factorys f WHERE f.id = %s', [id])
    data = cur.fetchall()
    cur.close() 
    return render_template('add_productFactory.html', factorys=data)

@app.route('/CreateProductFactory', methods=['GET', 'POST'])
def CreateProductFactory():
    if request.method == 'POST':
        name = request.form['name']
        stock = request.form['stock']
        price = request.form['price']  
        description = request.form['description']   
        id_factory = request.form.get('id_factory') 
            

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (name, stock, price,description) VALUES (%s,%s,%s,%s)",
                    (name, stock, price,description))
        flash('Contact Updated Successfully')
        mysql.connection.commit()


        cur = mysql.connection.cursor()
        cur.execute('select p.id  from products p order by p.ID desc limit 1')
        id_product = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('select p.name  from products p order by p.ID desc limit 1')
        name_product = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO factorys_products VALUES (%s,%s,%s)",
                    (id_factory, id_product,name_product))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/viewPruductosFactory/<id>')
def getPruductosFactory(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products p join factorys_products fp on p.ID = fp.ID_product join factorys f on f.ID = fp.ID_factory where fp.ID_factory = %s', [id])
    data = cur.fetchall()
    cur.close()

    return render_template('viewPruductosFactory.html', Factorys=data)

@app.route('/edit_product/<id>', methods=['POST', 'GET'])
def edit_product(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    return render_template('edit_product.html', products=data[0])

@app.route('/updateProduct/<id>', methods=['POST'])
def updateProduct(id):
    if request.method == 'POST':
        name = request.form['name']
        stock = request.form['stock']
        price = request.form['price']
        description = request.form['description']
        

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE products
            SET name = %s,
                stock = %s,
                price = %s,
                description = %s
            WHERE id = %s
        """, (name, stock, price, description ,id))
        flash('Contact Updated Successfully')

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE factorys_products
            SET name_product = %s
            WHERE id_product = %s
        """, (name,id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete_product/<id>', methods=['POST', 'GET'])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM products WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

@app.route('/view_products')
def view_products():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    data = cur.fetchall()
    cur.close()

    flash('Contact Added successfully')
    return render_template('view_products.html', products = data)


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
