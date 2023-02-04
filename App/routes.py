from flask import render_template, request, redirect, url_for, session
import re
import MySQLdb.cursors
from App.confi import *

@app.route('/')
def home():
    with connection.cursor() as cursor:
        # Fetch all the products from the products table
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    return render_template('home..html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():

    mesage = ''
    if 'loggedin' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return redirect(url_for('home'))
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage=mesage)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    session.pop('address', None)
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if 'loggedin' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s, % s)', (userName, email, password,address))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage=mesage)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'loggedin' in session:
        if request.method == 'POST':
            # Update user's profile in the database
            name = request.form['name']
            email = request.form['email']
            address = request.form['address']
            with connection.cursor() as cursor:
                cursor.execute("UPDATE user SET name=%s, email=%s, address=%s WHERE userid=%s",
                               (name, email, address, session['userid']))
                connection.commit()
            return redirect(url_for('profile'))

        # Fetch the order history from the orders table for the current user
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE userid=%s", (session['userid']))
        order_history = cursor.fetchall()
        cursor.close()

        return render_template('user.html', order_history=order_history)
    else:
        return redirect(url_for('login'))


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        # Update user's profile in the database
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        with connection.cursor() as cursor:
            cursor.execute("UPDATE user SET name=%s, email=%s, address=%s WHERE userid=%s", (name, email, address, session['userid']))
            connection.commit()
            # update session variables
            session['name'] = name
            session['email'] = email
            session['address'] = address
            mesage = 'Your Profile has been updated successfully'
        return redirect(url_for('profile',mesage=mesage))

    return render_template('edit_profile.html')

@app.route('/delete_profile', methods=['GET', 'POST'])
def delete_profile():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Delete user's profile from the database
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM user WHERE userid=%s", (session['userid'],))
            connection.commit()
            session.pop('loggedin', None)
            session.pop('userid', None)
            session.pop('email', None)
        return redirect(url_for('home'))
    if 'userid' not in session:
        return redirect(url_for('login'))


@app.route('/cart')
def cart():
    # Check if user is logged in
    if 'userid' not in session:
        return redirect(url_for('login'))

    user_id = session['userid']
    # Get the products from the database that are in the user's cart
    cursor = connection.cursor()
    query = "SELECT * FROM cart WHERE userid=%s"
    cursor.execute(query, (user_id,))
    items = cursor.fetchall()

    total_price = sum([item['total_price'] for item in items])


    return render_template('cart.html', items=items, total_price=total_price)



@app.route('/checkout')
def checkout():
    return render_template("checkout.html")


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'userid' not in session:
        return redirect(url_for('login'))

    product_id = request.form['productid']
    userid = int(session['userid'])
    product_name = request.form['pname']
    if request.form['quantity']:
        quantity = int(request.form['quantity'])
    else:
        # set the default quantity to 1
        quantity = 1

    size = request.form['size']
    price = float(request.form['productprice'])
    total_price = quantity * price

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM cart WHERE userid=%s AND productid=%s", (userid, product_id))
        result = cursor.fetchone()
        if result:
            updated_quantity = result['quantity'] + quantity
            updated_total_price = updated_quantity * price
            cursor.execute("UPDATE cart SET quantity=%s, total_price=%s WHERE userid=%s AND productid=%s", (updated_quantity, updated_total_price, userid, product_id))
        else:
            cursor.execute("INSERT INTO cart (userid, pname, productid, quantity, size, productprice, total_price) VALUES (%s, %s, %s, %s, %s, %s, %s)", (userid, product_name, product_id, quantity, size, price, total_price))
        connection.commit()

    if 'cart' not in session:
        session['cart'] = {}

    session['cart'][product_id] = {
        'quantity': quantity,
        'pname': product_name,
        'size': size,
        'productprice': price,
        'total_price': total_price
    }

    return redirect(url_for('cart'))


@app.route('/remove_from_cart/<product_id>', methods=['GET', 'POST'])
def remove_from_cart(product_id):
    if 'userid' not in session:
        return redirect(url_for('login'))

    user_id = session['userid']
    cursor = connection.cursor()
    query = "DELETE FROM cart WHERE userid=%s AND productid=%s"
    cursor.execute(query, (user_id, product_id))
    connection.commit()

    return redirect(url_for('cart'))


@app.route('/order_confirmation')
def order_confirmation():
    return render_template("order_confirmation.html")

@app.route("/submit-order", methods=["POST"])
def submit_order():
    # Retrieve the form data from the request
    name = request.form.get("name")
    email = request.form.get("email")
    address = request.form.get("address")
    card_number = request.form.get("card-number")
    expiry = request.form.get("expiry")
    cvv = request.form.get("cvv")

    # Get the user ID from the session
    user_id = session.get("userid")

    # Retrieve the items in the cart for the user
    mysql = "SELECT * FROM cart WHERE userid = %s"
    cursor.execute(mysql, (user_id,))
    items = cursor.fetchall()

    # Insert the order details into the orders table
    for item in items:
        mysql = "INSERT INTO orders (userid, product_id, quantity, size, price, total) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(mysql, (user_id, item['productid'], item['quantity'], item['size'], item['productprice'], item['total_price']))

    # Delete the items from the cart
    mysql = "DELETE FROM cart WHERE userid = %s"
    cursor.execute(mysql, (user_id,))

    # Remove items from session cart
    session.pop("cart", None)

    # Commit the changes and close the connection
    connection.commit()

    # Return a response to the client
    return redirect(url_for('order_confirmation'))
