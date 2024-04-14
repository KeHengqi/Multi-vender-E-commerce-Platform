import pymysql
from hashlib import sha256
# If you want to specify the database_login_user, please goto
# global_profile
from global_profile import database_login_user

db = pymysql.connect(host='localhost',
                     user=database_login_user.name,
                     password=database_login_user.password,
                     database=database_login_user.database)
 
username = 'testing'
password = '1234'
salt = 1 #generate a CPRN
hashed_pw = sha256(str.encode(password + str(salt))).hexdigest()

cursor = db.cursor()

sql = '''
    INSERT INTO vAdmin (username, password, salt)
    VALUES (%s, %s, %s)
'''

# Structure of customer
# cid INTEGER NOT NULL AUTO_INCREMENT,
# contactNumber INTEGER(8) NOT NULL,
# shippingDetail CHAR(20) NOT NULL,
# username VARCHAR(50) NOT NULL,
# password CHAR(255) NOT NULL,
# salt INTEGER NOT NULL,
# PRIMARY KEY(cid)

user_phone = 12345678
address = 'HKBU'
user_name = 'kevin'
user_password = '1234567890'
hashed_user_pw = sha256(str.encode(user_password + str(salt))).hexdigest()

sql_customer = '''
    INSERT INTO Customer (contactNumber, shippingDetail, username, password, salt)
    VALUES (%s, %s, %s, %s, %s)
'''

cursor.execute(sql, (username, hashed_pw, salt))
cursor.execute(sql_customer, (user_phone, address, user_name, hashed_user_pw, salt))

cursor.close()
db.commit()
db.close()