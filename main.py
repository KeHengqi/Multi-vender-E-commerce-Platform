from flask import Flask, render_template, request, redirect, url_for, session, flash
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
#import MySQLdb.cursors, re, hashlib
import pymysql
from hashlib import sha256
from global_profile import database_login_user
from json import dump
from query import db
import query
from datetime import datetime


# In different environment, the usename of database and password may be
# different, you can specify your name, password and database in the
# database_login_user

# comment here
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = database_login_user.name
app.config['MYSQL_PASSWORD'] = database_login_user.password
app.config['MYSQL_DB'] = database_login_user.database
app.secret_key = 'hihi'

mysql = pymysql.connect(
    host = app.config['MYSQL_HOST'],
    user = app.config['MYSQL_USER'],
    password= app.config['MYSQL_PASSWORD'],
    db = app.config['MYSQL_DB']
)

# Functional check method
@app.route('/check_username', methods=['POST'])
def check_username():
    # check if user already exists
    username = request.json['username']
    cursor = mysql.cursor()
    cursor.execute(query.checkUsername(), (username,))
    data = cursor.fetchone()
    if data:
        return {'is_taken': True}
    return {'is_taken': False}

@app.route('/product_update_data', methods=['POST'])
def product_update_data():
    # Update product information
    pid = request.json['pid']
    price = request.json['price']
    # vid = request.json['vid']
    p_tag1 = request.json['p_tag1']
    p_tag2 = request.json['p_tag2']
    p_tag3 = request.json['p_tag3']
    inventory = request.json['inventory']
    cursor = mysql.cursor()
    cursor.execute(query.updateProduct(), (price, inventory, p_tag1, p_tag2, p_tag3, pid))
    mysql.commit()
    return {'success': True}

@app.route('/product_add_data', methods=['POST'])
def product_add_data():
    # Add new product
    cursor = mysql.cursor()
    cursor.execute(query.browseVendorByVname(), (request.json['vname'],))
    vendor = cursor.fetchone()
    vid = vendor[0]
    pname = request.json['pname']
    price = request.json['price']
    # vid = session['vendor_id']
    p_tag1 = request.json['p_tag1']
    p_tag2 = request.json['p_tag2']
    p_tag3 = request.json['p_tag3']
    inventory = request.json['inventory']
    cursor = mysql.cursor()
    cursor.execute(query.addProduct(), (pname, price, vid, inventory, p_tag1, p_tag2, p_tag3, ''))
    mysql.commit()
    return {'success': True}

@app.route('/vendor_add_data', methods=['POST'])
def vendor_add_data():
    # Add new vendor
    vname = request.json['vname']
    # password = request.json['password']
    geographic = request.json['vgeographic']
    vpassword = vname + '2024'
    password = sha256(str.encode(vpassword + str(1))).hexdigest()
    score = request.json['vscore']
    cursor = mysql.cursor()
    cursor.execute(query.addVendor(), (vname, score, geographic, password, '1'))
    mysql.commit()
    return {'success': True}

@app.route('/get_new_pid', methods=['POST'])
def get_new_pid():
    # Increment product ID
    cursor = mysql.cursor()
    cursor.execute(query.getNewPid())
    data = cursor.fetchone()
    print(data)
    return {'pid': str(int(data[0]) + 1)}

@app.route('/get_new_vid', methods=['POST'])
def get_new_vid():
    # Increment vendor ID
    cursor = mysql.cursor()
    cursor.execute(query.getNewVid())
    data = cursor.fetchone()
    print(data)
    return {'vid': str(int(data[0]) + 1)}

@app.route('/add_cart/<customer_id>', methods=['POST'])
def add_cart(customer_id):
    # Add products to cart
    cursor = mysql.cursor()
    product_name = request.json['product_name']
    print(product_name)
    cursor.execute(query.browseProductByPname(), (product_name,))
    # cursor.execute(query.browseProductByPid(), (product_id,))
    product = cursor.fetchone()
    pid = product[0]
    # print(pid)
    cursor.execute(query.addCart(), (customer_id, pid, 1))
    mysql.commit()
    return {'success': True}

@app.route('/delete_cart/<customer_id>', methods=['POST'])
def delete_cart(customer_id):
    # Delete product from cart
    cursor = mysql.cursor()
    product_name = request.json['product_name']
    cursor.execute(query.browseProductByPname(), (product_name,))
    product = cursor.fetchone()
    pid = product[0]
    cursor.execute(query.deleteCart(), (customer_id, pid))
    mysql.commit()
    return {'success': True}

@app.route('/update_cart/<customer_id>', methods=['POST'])
def update_cart(customer_id):
    # Update products in cart
    cursor = mysql.cursor()
    product_name = request.json['product_name']
    cursor.execute(query.browseProductByPname(), (product_name,))
    product = cursor.fetchone()
    pid = product[0]
    quantity = request.json['quantity']
    cursor.execute(query.updateCart(), (quantity, customer_id, pid))
    mysql.commit()
    return {'success': True}

@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    cursor = mysql.cursor()
    oid = request.json['oid']
    status = request.json['status']
    product_name = request.json['product_name']
    print(oid, status, product_name)
    cursor.execute(query.browseProductByPname(), (product_name,))
    product = cursor.fetchone()
    pid = product[0]
    cursor.execute(query.updateOrderProductStatus(), (status, oid, pid))
    mysql.commit()
    return {'success': True}

@app.route('/logout')
def logout():
    # Logout account
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('customer_id', None)
    session.pop('customer_name', None)
    session.pop('vendor_id', None)
    session.pop('vendor_name', None)
    session.pop('vendor_score', None)
    session.pop('vendor_geographic', None)
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    return redirect(url_for('loginOrRegister'))

@app.route('/search_product', methods=['GET', 'POST'])
def search_product():
    # Search for products
    pname = request.form['search_info']
    # pname = request.json['search_info']
    # print(pname)
    search_info = '%' + pname + '%'
    # print(search_info)
    # mysql.connect()
    cursor = mysql.cursor()

    exe_str = cursor.mogrify(query.searchProductByNameAndTag(), (search_info, search_info, search_info, search_info))
    # print(exe_str)
    cursor.execute(exe_str)
    data = cursor.fetchall()
    datalist = list(data)

    hint_word = set_hint_word()
    customer_name = set_customer_name()
    customer_id = session['customer_id']
    # print(data)
    return render_template('products.html', data=datalist, hint_word=hint_word, customer_name=customer_name, customer_id=customer_id)

@app.route('/remove_all_from_cart/<customer_id>', methods=['POST'])
def remove_all_from_cart(customer_id):
    # Remove all products from cart
    cursor = mysql.cursor()
    cursor.execute(query.deleteCartByCid(), (customer_id,))
    mysql.commit()
    return {'success': True}

# Page represent function
# Kinney route
@app.route('/cart_page/<customer_id>', methods=['GET', 'POST'])
def cart_page(customer_id):
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute(query.browseCustomerByCid(), (customer_id,))
        data = cursor.fetchone()
        print(data)
        cursor.execute(query.browseCartProductsByCid(), (customer_id,))
        products = cursor.fetchall()
        return render_template('cart_page.html', customer_id=customer_id, customer_name=data[3], products = products, no_product=False)
    return redirect(url_for('loginOrRegister'))

@app.route('/customer_page/<customer_id>')
def customer_page(customer_id):
     # Check if the user is logged in
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute(query.browseCustomerByCid(), (customer_id,))
        # cursor.execute(query.browseAllProductsByCustomer(), (session['customer_name'],))
        data = cursor.fetchone()
        # User is loggedin show them the home page
        return render_template('customer_page.html',customer_id=customer_id, customer_name=data[3], customer_address=data[2], customer_phone=data[1])
    # User is not loggedin redirect to login page
    return redirect(url_for('loginOrRegister'))

@app.route('/order_page/<customer_id>', methods=['GET', 'POST'])
def order_page(customer_id):
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute(query.browseCustomerByCid(), (customer_id,))
        data = cursor.fetchone()

        # get all order ids of the customer
        cursor.execute(query.browseAllOrdersByCid(), (customer_id,))
        order_ids = cursor.fetchall()
        # print(order_ids)
        list_order_ids = list(order_ids)
        # print(list_order_ids)
        orders_list = []
        for oid in list_order_ids:
            print(oid[0])
            order_dict = {}
            # may have wrong
            order_dict['oid'] = oid[0]
            cursor.execute(query.browseAllOrdersProductsByOidCid(), (oid[0], customer_id,))
            products = cursor.fetchall()
            order_dict['products'] = list(products)
            sum = 0
            for product in products:
                sum += product[1] * product[5]
            order_dict['total_price'] = sum
            orders_list.append(order_dict)
            # print(order_dict)
        print(orders_list)
            
        return render_template('order_page.html', customer_id=customer_id, customer_name=data[3], orders=orders_list)
    return redirect(url_for('loginOrRegister'))

@app.route('/order_page_all', methods=['GET', 'POST'])
def order_page_all():
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute(query.browseAllOrdersOid())
        oid_list = list(cursor.fetchall())
        orders_list = []
        for oid in oid_list:
            order_dict = {}
            order_dict['oid'] = oid[0]
            cursor.execute(query.browseAllOrdersProductsByOid(), (oid[0],))
            products = cursor.fetchall()
            order_dict['products'] = list(products)
            sum = 0
            for product in products:
                sum += product[1] * product[5]
            order_dict['total_price'] = sum
            orders_list.append(order_dict)
        return render_template('order_page_all.html', orders=orders_list)
    return redirect(url_for('loginOrRegister'))

@app.route('/buy_products/<customer_id>', methods=['GET', 'POST'])
def buy_products(customer_id):
    cursor = mysql.cursor()
    cursor.execute(query.browseCartProductsByCid(), (customer_id,))
    products = cursor.fetchall()
    no_product = False
    if len(products) == 0:
        no_product = True
        flash('No product in the cart!')
        return redirect(url_for('cart_page', customer_id=customer_id, no_product=no_product))
    else:
        # Get the latest order id
        cursor.execute(query.getMaxOid())
        max_oid = cursor.fetchone()
        print(max_oid)
        latest_oid = 0
        if max_oid[0] == None:
            print('None')
            latest_oid = 1
        else:
            latest_oid = int(max_oid[0]) + 1

        time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        flag = 0
        for product in products:
            cursor.execute(query.browseProductByPid(), (product[1],))
            product_garage = cursor.fetchone()
            Inventory = product_garage[4]
            if Inventory != 0:
                if Inventory - product[2] < 0:
                    flash(product_garage[1] + ' Inventory is not enough!')
                    flag = 1
                else:
                    cursor.execute(query.addOrder(), (latest_oid, customer_id, product[1], product[2], time_stamp))
                    cursor.execute(query.deleteCart(), (customer_id, product[1]))
                    cursor.execute(query.updateInventory(), (Inventory - product[2], product[1]))
            else:
                flash(product_garage[1] + ' Inventory is 0')
                flag = 1
        mysql.commit()
        if flag == 0:
            flash('Order success!')
            return redirect(url_for('order_page', customer_id=customer_id))
        else:
            return redirect(url_for('cart_page', customer_id=customer_id))

@app.route('/vendor_page/<vendor_id>')
def vendor_page(vendor_id):
    if 'loggedin' in session:
        # cursor = mysql.cursor()
        # cursor.execute(query.browseAllProductsByVendor(), (session['vendor_name'],))
        # data = cursor.fetchall()
        # print(session['vendor_score'])
        hint_word = set_hint_word_vendor()
        
        cursor = mysql.cursor()
        cursor.execute(query.browseVendorByVid(), (vendor_id,))
        data = cursor.fetchone()

        return render_template('vendor_page.html', vendor_id=vendor_id ,vendor_name=data[1], vendor_score=data[2], vendor_geographic=data[3], hint_word=hint_word)
    return redirect(url_for('loginOrRegister'))

@app.route('/admin_page')
def admin_page():
    if 'loggedin' in session:
        # cursor = mysql.cursor()
        # cursor.execute(query.browseAllProducts())
        # data = cursor.fetchall()
        return render_template('admin_page.html', admin_name=session['admin_name'], admin_id=session['admin_id'])
    return redirect(url_for('loginOrRegister'))

@app.route('/v_p_list/<vendor_id>')
def v_p_list(vendor_id):
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute(query.browseVendorByVid(), (vendor_id,))
        vendor = cursor.fetchone()
        vendor_name = vendor[1]
        cursor.execute(query.browseAllProductsByVendor(), (vendor_name,))
        data = cursor.fetchall()
        hint_word = set_hint_word()
        return render_template('vendor_product_list.html', products=data, hint_word=hint_word, vendor_name=vendor_name)
    return redirect(url_for('login'))
    # return render_template('vendor_product_list.html')

@app.route('/vendor_list')
def vendor_list():
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute(query.browseAllVendors())
        data = cursor.fetchall()
        return render_template('vendor_list.html', vendors=data, admin_name=session['admin_name'])
    return redirect(url_for('login'))

# Kinney route
@app.route('/vAdmin', methods=['GET', 'POST'])
# John route
# @app.route('/pythonlogin/', methods=['GET', 'POST'])
def admin_login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        # TODO: Need to update the salt here
        password = sha256(str.encode(password + str(1))).hexdigest()

        # Check if account exists using MySQL
        cursor = mysql.cursor()#.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vadmin WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]#['id']
            session['username'] = account[1]#['username']
            # Redirect to home page
            return redirect(url_for('vAdminHome'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('vAdmin.html', msg=msg)

@app.route('/')
def loginOrRegister():
    login_activate = "active"
    register_activate = ""
    return render_template('index.html', login_activate=login_activate, register_activate=register_activate)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    login_activate = "active"
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # DONE: realising getting the user type(customer/vendor)
        login_type = request.form.get('usertype')

        # print(dump(request.form))

        print(request.form.get('usertype'))

        # TODO: Need to update the salt here
        password = sha256(str.encode(password + str(1))).hexdigest()

        # Check if account exists using MySQL
        cursor = mysql.cursor()#.connection.cursor(MySQLdb.cursors.DictCursor)

        # Detect which type of user is logging in
        if login_type == 'customer':
            cursor.execute('SELECT * FROM Customer WHERE username = %s AND password = %s', (username, password))
        elif login_type == 'vendor':
            cursor.execute('SELECT * FROM Vendor WHERE vname = %s AND password = %s', (username, password))
        elif login_type == 'admin':
            cursor.execute('SELECT * FROM vAdmin WHERE username = %s AND password = %s', (username, password))
        
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
        # If account exists in accounts table in out database
        if account:
            session['loggedin'] = True
            if login_type == 'customer':
                session['customer_id'] = account[0]
                session['customer_name'] = account[3]#['customer_name']
                return redirect(url_for('products'))
            # Create session data, we can access this data in other routes
            elif login_type == 'vendor':
                session['vendor_id'] = account[0]#['vid']
                session['vendor_name'] = account[1]#['vname']
                session['vendor_score'] = account[2]#['score']
                session['vendor_geographic'] = account[3]#['geographic']
                # print('Here')
                return redirect(url_for('vendor_page', vendor_id=account[0]))
            elif login_type == 'admin':
                session['admin_id'] = account[0]#['id']
                session['admin_name'] = account[1]#['username']
                return redirect(url_for('admin_page'))
            # session['id'] = account[0]#['id']
            # session['username'] = account[1]#['username']
            # Redirect to home page
            
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg, login_activate=login_activate, register_activate="")

def set_hint_word():
    if 'customer_name' not in session or session['customer_name'] == '':
        return 'Please login first!'
    else:
        return 'Welcome back,'

def set_hint_word_vendor():
    if 'vendor_name' not in session or session['vendor_name'] == '':
        return 'Please login first!'
    else:
        return 'Welcome back,'

def set_customer_name():
    if 'customer_name' not in session or session['customer_name'] == '':
        return ''
    else:
        return session['customer_name']

@app.route('/products', methods=['GET', 'POST'])
def products():
    mysql.connect()
    cursor = mysql.cursor()
    cursor.execute(query.browseAllProducts())
    mysql.commit()
    data = cursor.fetchall()
    hint_word = set_hint_word()
    customer_name = set_customer_name()
    customer_id = session['customer_id']
    print(customer_id)

    return render_template('products.html', data=data, hint_word=hint_word, customer_name=customer_name, customer_id=customer_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    register_activate = "active"
    if request.method == 'POST' and 'reg_username' in request.form and 'reg_password' in request.form:
        if request.form.get('reg_password') != request.form.get('reg_re_password'):
            msg = 'Fuck you, what you are fucking doing?'
        else:
            # TODO: Input the message into the database

            username = request.form['reg_username']
            password = request.form['reg_password']
            phone = request.form['reg_phone']
            loc = request.form['reg_loc']

            usertype = request.form.get('reg_usertype')

            password = sha256(str.encode(password + str(1))).hexdigest()

            # Check if account exists using MySQL
            cursor = mysql.cursor()#.connection.cursor(MySQLdb.cursors.DictCursor)

            # Detect which type of user is logging in
            if usertype == 'customer':
                cursor.execute(query.addCustomer(), (phone, loc, username, password, '1'))
                mysql.commit()
            elif usertype == 'vendor':
                cursor.execute(query.addVendor(), (username, loc, password, '1'))
                mysql.commit()
            msg = 'Congras! Now you are one of the user'
            # # Fetch one record and return result
            # account = cursor.fetchone()
            # print(account)
            # # If account exists in accounts table in out database
            # if account:
            #     session['loggedin'] = True
            #     if login_type == 'customer':
            #         session['customer_name'] = account[3]#['customer_name']
            #         return redirect(url_for('customer_page'))
            #     # Create session data, we can access this data in other routes
            #     elif login_type == 'vendor':
            #         session['vendor_name'] = account[1]#['vname']

    # Show the login form with message (if any)
    return render_template('index.html', msg=msg, register_activate=register_activate, login_activate="")



if __name__ == '__main__':
    app.run(debug=True)