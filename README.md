# COMP7640_GroupProject
 
# TODO

- Vendor Administration
    - [x] Display a listing of all vendors
    - [x] Onboard new vendors onto the marketplace
- Product Catalog Management
    - [x] Browse all products offered by a specific vendor
    - [x] Introduce new products to a vendor's catalog
- Product Discovery
    - [x] Facilitate a search feature that allows users to discover products using tags,
    the search should return products where the tag matches any part of the product's name or its associated tags
- Product Purchase
    - [x] You should support product purchase. Record in database which customer purchases which product
- Order Modification
    - [ ] Users must have the option to modify their orders, including the removal of specific products or the cancellation of the entire order before it enters the shipping process
	
# Requirements
- Python 3.11
- [Optional] Virtual environment such as conda:
```
	conda create -n comp7640 python=3.11
```
# Installing dependencies
- Run pip install to install dependencies:
```
	pip install -r requirements.txt
```

# Setting up MySQL database	
- Go to MySQL workbench and create a database called 'ecommerce':
```
	CREATE DATABASE ecommerce;
```

- Go to global_profile.py and enter your MySQL credential:
```
	database_login_user = SqlAdmin(username, password, 'ecommerce')
```
Where username and password are your MySQL user and password respectively.

- To create the required tables, run initDB.py:
```
	python initDB.py
```

- [Optional] To change the password for Vendor Admin login, go to setVendorAdminCredential.py and change the values for the variables 'username' and 'password', the default values are 'testing' and '1234' respectively.
 
- To set up a vendor admin login credential, run setVendorAdminCredential.py:
```
	python setVendorAdminCredential.py
```
- To launch the website, run main.py:
```
	python main.py
```

- Go to http://127.0.0.1:5000 for the login and register page.

# Logging in Vendor Admin page
- Click the 'Login' tab, choose 'Admin' from the dropdown menu.
- Enter the username and password for Vendor Admin page, default values are 'testing' and '1234' respectively.
- Click the 'Login' button.

![](/img/admin_login.JPG)

# Vendor Administration
- Click "Go to vendor list" to view the list of all vendors.
- To onboard a new vendor, click "Add Vendor", enter the fields for "Business Name", "Score", and "Address", click "Save".



# Registering a Vendor account
- To register for a vendor account, go back to the home page and click "Register" tab (http://127.0.0.1:5000/register).
- Select "Vendor" from the drop down menu, enter the vendor information (username, password, location, phone number).
- Click "Register".
- There are some initial vendor accounts specified in initDB.py. For example, you can login with the username 'Apple' and password 'apple2024'.
- The corresponding Python code for initializing these accounts are given below:
```
    apple_password = 'apple2024'
    samsung_password = 'samsung2024'
    xiaomi_password = 'xiaomi2024'
    huawei_password =  'huawei2024'
    nvidia_password = 'nvidia2024'
    amd_password = 'amd2024'
    # TODO: Need to update the salt here
    apple_hashed_password = sha256(str.encode(apple_password + str(1))).hexdigest()
    samsung_hashed_password = sha256(str.encode(samsung_password + str(1))).hexdigest()
    xiaomi_hashed_password = sha256(str.encode(xiaomi_password + str(1))).hexdigest()
    huawei_hashed_password = sha256(str.encode(huawei_password + str(1))).hexdigest()
    nvidia_hashed_password = sha256(str.encode(nvidia_password + str(1))).hexdigest()
    amd_hashed_password = sha256(str.encode(amd_password + str(1))).hexdigest()

    cursor.execute(query.addVendor(), ('Apple', 4.9, 'California, USA', apple_hashed_password, 1))
    cursor.execute(query.addVendor(), ('Samsung', 4.8, 'Seoul, Korea', samsung_hashed_password, 1))
    cursor.execute(query.addVendor(), ('Xiaomi', 4.7, 'Beijing, China', xiaomi_hashed_password, 1))
    cursor.execute(query.addVendor(), ('Huawei', 4.6, 'Shenzhen, China', huawei_hashed_password, 1))
    cursor.execute(query.addVendor(), ('Nvidia', 4.9, 'California, USA', nvidia_hashed_password, 1))
    cursor.execute(query.addVendor(), ('AMD', 4.8, 'California, USA', amd_hashed_password, 1))
```

# Product Catalog Management
- To browse the products offered by a specific vendor, login a vendor account.
- Go back to the login page and select "Vendor" from the drop down menu.
- Login with one of the vendor credential given in the previous step, or the one you registered. 
- Click "View Product" to browse all products offered by the vendor account you logged in.
- To introduce new products to the vendor's catalog, click "Add Product" and fill in the product information 
(Product Name, Listed Price/HKD, Product Tag1, Product Tag2, Product Tag3, Inventory/Unit), click "Save".
 
# Registering a Customer Account
- To register for a customer account, go back to the home page and click "Register" tab (http://127.0.0.1:5000/register).
- Select "Customer" from the drop down menu, enter the customer information (username, password, location, phone number).
- Click "Register".
- You should see "Congras! Now you are one of the user" if successful.

# Product Discovery
- Go back to the login page , select "Customer" and login with the credential you created.
- To discover products using tags, enter a tag in the search bar and click the "magnifier" icon.

![](/img/search.JPG)

- For example, entering "Apple" in the search bar and search, it will return all Apple products.
- The search function also support partial matching, for example, entering "app" or "ple" will also return
all Apple products, while entering "sam" will return all Samsung products.
- You can also discover products by their names or partial names. For example, entering "book" will return all products
with names containing "book", including "Galaxy Book", "MacBook Pro", "MateBook", etc. 
- You can also discover products using their exact names, for example, entering "MacBook Pro" will only return the product "MacBook Pro".


# Product Purchase

