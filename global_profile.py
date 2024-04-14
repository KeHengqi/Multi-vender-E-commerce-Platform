class SqlAdmin:
    name = "test"
    password = "1234567890-="
    database = "ecommerce"

    # `name` input mysql's username, `password` input the mysql's password,
    # `database` input mysql's database
    def __init__(self, name, password, database):
        self.name = name
        self.password = password
        self.database = database

# Kinney user
# database_login_user = SqlAdmin('root', '321Misaka@khq', 'ecommerce')

# John user
# database_login_user = SqlAdmin('test', '1234567890-=', 'ecommerce')

database_login_user = SqlAdmin('root', '2242Lwy!', 'ecommerce')
        