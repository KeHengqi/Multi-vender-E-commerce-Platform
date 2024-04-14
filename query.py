import pymysql
from global_profile import database_login_user
from hashlib import sha256

db = pymysql.connect(host='localhost',
                     user=database_login_user.name,
                     password=database_login_user.password,
                     database=database_login_user.database)
 


cursor = db.cursor()

# TODO: Change the following functions from in-function execute to return the sql string

# Check class function

 # check if user already exists
def checkUsername():
    sql = '''
    SELECT * FROM Customer
    WHERE username = %s '''
    return sql

# browse all products
def browseAllProducts():
    sql = '''
    SELECT * FROM Product
    '''
    return sql

# browse all vendors
def browseAllVendors():
    sql = '''
    SELECT * FROM Vendor
    '''
    return sql
# browse vendors by vendor ID
def browseVendorByVid():
    sql = '''
    SELECT * FROM Vendor
    WHERE vid = %s
    '''
    return sql
# browse vendors by vendor name
def browseVendorByVname():
    sql = '''
    SELECT * FROM Vendor
    WHERE vname = %s
    '''
    return sql
# browse customer by customer ID
def browseCustomerByCid():
    sql = '''
    SELECT * FROM Customer
    WHERE cid = %s
    '''
    return sql
# browse product by product name
def browseProductByPname():
    sql = '''
    SELECT * FROM Product
    WHERE pname = %s
    '''
    return sql

def browseProductByPid():
    sql = '''
    SELECT * FROM Product
    WHERE pid = %s
    '''
    return sql

# browse product in cart by customer ID
def browseCartProductsByCid():
    sql = '''
    WITH TMP AS
        (SELECT Cart.*, pname, price FROM Cart INNER JOIN Product 
            ON Cart.pid = Product.pid)
    SELECT TMP.* FROM TMP 
            WHERE cid = %s;
    '''
    return sql

# browse all products offered by a specific vendor
def browseAllProductsByVendor():
    sql = '''
    WITH TMP AS 
        (SELECT Product.*, Vendor.vname FROM Product, Vendor
        WHERE Product.vid = Vendor.vid)
    SELECT * FROM TMP
    WHERE vname = %s
    '''
    # cursor.execute(sql,(vname,))
    return sql

# browse all products by customer
def browseAllProductsByCustomer():
    sql = '''
    WITH TMP AS
        (SELECT Ordered.*, pname FROM Ordered INNER JOIN Product 
            ON Ordered.pid = Product.pid)

    SELECT TMP.*, username FROM TMP INNER JOIN Customer 
            ON TMP.cid = Customer.cid
            WHERE username = %s;
    '''
    # cursor.execute(sql,(cname,))
    return sql

# browse all order by customer ID
def browseAllOrdersByCid():
    sql = '''
    SELECT oid FROM Ordered
    WHERE cid = %s
    GROUP BY oid
    '''
    return sql

# browse all order by order ID and customer ID
def browseAllOrdersOid():
    sql = '''
    SELECT oid FROM Ordered
    GROUP BY oid
    '''
    return sql

def browseAllOrdersProductsByOid():
    sql = '''
    WITH TMP AS
        (SELECT pname, price, Ordered.* FROM Ordered INNER JOIN Product 
            ON Ordered.pid = Product.pid)
    SELECT TMP.* FROM TMP
    WHERE oid = %s
    '''
    return sql

def browseAllOrdersProductsByOidCid():
    sql = '''
    WITH TMP AS
        (SELECT pname, price, Ordered.* FROM Ordered INNER JOIN Product 
            ON Ordered.pid = Product.pid)
    SELECT TMP.* FROM TMP
    WHERE oid = %s AND cid = %s
    '''
    return sql

# Add vendor ID by vendor name
def getVid():
    sql = '''
    SELECT vid FROM Vendor
    WHERE vname = %s
    '''
    return sql
# Get latest pid to increment it
def getNewPid():
    sql = '''
    SELECT MAX(pid) FROM Product
    '''
    return sql
# Get latest vid to increment it
def getNewVid():
    sql = '''
    SELECT MAX(vid) FROM Vendor
    '''
    return sql
# Get latest oid to increment it
def getMaxOid():
    sql = '''
    SELECT MAX(oid) FROM Ordered
    '''
    return sql


# Check class function end
# =================================================================================================

# Update class function
# Onboard new vendors onto the marketplace
def addVendor():
    # password = sha256(str.encode(password + str(salt))).hexdigest()
    sql = '''
    INSERT INTO Vendor(vname, score, geographic, password, salt)
    VALUES (%s,%s,%s,%s,%s)
    '''
    return sql
# Add new customer
def addCustomer():
    # password = sha256(str.encode(password + str(salt))).hexdigest()
    sql = '''
    INSERT INTO Customer(contactNumber, shippingDetail, username, password, salt)
    VALUES (%s,%s,%s,%s,%s)
    '''
    return sql

# Introduce new products to a vendor's catalog
def addProduct():
    sql = '''
    INSERT INTO Product(pname, price, vid, inventory, tag1, tag2, tag3, url) 
    VALUES (%s,%s,%s,%s, %s, %s, %s, %s)
    '''
    return sql
# Add product to cart
def addCart():
    sql = '''
    INSERT INTO Cart(cid, pid, quantity)
    VALUES (%s,%s,%s)
    '''
    return sql
# Add admin account credential
def addAdmin():
    sql = '''
    INSERT INTO vAdmin(username, password, salt)
    VALUES (%s,%s,%s)
    '''
    return sql
# Add order by a customer
def addOrder():
    sql = '''
    INSERT INTO Ordered(oid, cid, pid, quantity, orderStatus, orderTime)
    VALUES (%s,%s,%s,%s,'order received',%s)
    '''
    return sql
# Update product information
def updateProduct():
    sql = '''
    UPDATE Product
    SET price = %s, inventory = %s, tag1 = %s, tag2 = %s, tag3 = %s
    WHERE pid = %s
    '''
    return sql
# Update product in cart, i.e. update quantity
def updateCart():
    sql = '''
    UPDATE Cart
    SET quantity = %s
    WHERE cid = %s AND pid = %s
    '''
    return sql

def updateInventory():
    sql = '''
    UPDATE Product
    SET inventory = %s
    WHERE pid = %s
    '''
    return sql

def updateOrderProductStatus():
    sql = '''
    UPDATE Ordered
    SET orderStatus = %s
    WHERE oid = %s AND pid = %s
    '''
    return sql

def deleteCart():
    sql = '''
    DELETE FROM Cart
    WHERE cid = %s AND pid = %s
    '''
    return sql
# Delete a customer's cart by customer id
def deleteCartByCid():
    sql = '''
    DELETE FROM Cart
    WHERE cid = %s
    '''
    return sql
# Update class function end
# =================================================================================================



# Facilitate a search feature that allows users to discover products using tags, 
# the search should return products where the tag matches any part of the product's
# name or its associated tags
def searchProductByName():
    sql = '''
    SELECT * FROM Product WHERE pname LIKE %s
    '''
    # print(sql)
    return sql

def searchProductByTag():
    sql = '''
    SELECT * FROM Product
    WHERE tag1 LIKE %s OR tag2 LIKE %s OR tag3 LIKE %s
    '''
    return sql

def searchProductByNameAndTag():
    sql = '''
    SELECT * FROM Product
    WHERE pname LIKE %s OR tag1 LIKE %s OR tag2 LIKE %s OR tag3 LIKE %s
    '''
    return sql

# Customer Register
def register(contactNumber, shippingDetail, username, password, salt):
    password = sha256(str.encode(password + str(salt))).hexdigest()
    sql = '''
    INSERT INTO Customer(contactNumber, shippingDetail, username, password, salt)
    VALUES (%s,%s,%s,%s,%s)
    '''
    cursor.execute(sql,(contactNumber, shippingDetail, username, password, salt))
    db.commit()



# support product purchase. Record in database which customer purchases which product
def purchase(cid, pid, quantity, orderTime):
    orderStatus = 'order received'
    sql = '''
    INSERT INTO Ordered(cid, pid, quantity, orderStatus, orderTime)
    VALUES (%s,%s,%s,%s,%s)
    '''
    cursor.execute(sql,(cid, pid, quantity, orderStatus, orderTime))
    db.commit()
 


# cancellation of the entire order before it enters the shipping process
def cancelOrder(oid):
    cursor.execute('''
        SELECT orderStatus 
        FROM Ordered
        WHERE oid = %s
    ''', (oid,))
    status = cursor.fetchone()

    sql = '''
    UPDATE Ordered
    SET orderStatus = 'cancelled'
    WHERE oid = %s
    '''
    # only execute cancel order if the orderStatus is not 'shipping' nor 'fulfilled' nor 'cancelled'
    if status == 'order received':
        cursor.execute(sql,(oid,))
        db.commit()



# the removal of specific products
def removeProduct(oid,pid):
    cursor.execute('''
        SELECT orderStatus 
        FROM Ordered
        WHERE oid = %s AND pid = %s
    ''', (oid,pid))

    status = cursor.fetchone()
    sql = '''
    DELETE FROM Ordered
    WHERE oid = %s AND pid = %s
    '''
    # only execute remove product if the orderStatus is not 'shipping' nor 'fulfilled' nor 'cancelled'
    if status == 'order received':
        cursor.execute(sql, (oid,pid))
        db.commit()
