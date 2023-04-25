# shopping-website

![image](https://user-images.githubusercontent.com/72424558/234277803-281be9e5-a24a-419c-8773-8b1c659f8eee.png)

## Heroku URL

https://shopping-website.herokuapp.com/

## Description

This website is developed with Django.
The requirement was creation of shopping website, so I chose the data which has image data because it makes good view
for visitor. The theme of website is "The apparel portal", that allows users to order items across a range of brands.

This website has some pages, access permission is managed by user role of login user.

### For All User

* [/](https://shopping-website.herokuapp.com/) ... Show all product list.
* [/detail/<item_id>](https://shopping-website.herokuapp.com/detail/43993) ... Show product detail and add product to
  cart.
* [/signup](https://shopping-website.herokuapp.com/signup) ... Sign up customer user.
* [/signin](https://shopping-website.herokuapp.com/signin) ... Sign in by username and password.

### For Customer User

* [/profile](https://shopping-website.herokuapp.com/profile) ... Customer can update user profile.
* [/order_list](https://shopping-website.herokuapp.com/order_list) ... Show all order history which login customer made.
* [/order/<order_id>](https://shopping-website.herokuapp.com/order/???) ... Show order detail of selected order.
* [/thanks/<order_id>](https://shopping-website.herokuapp.com/thanks/???) ... Thanks page for order.
* [/basket](https://shopping-website.herokuapp.com/basket) ... Show current basket and proceed purchase.
* [/purchase](https://shopping-website.herokuapp.com/purchase) ... Input payment information to complete an order.

### For Staff User(Administrator)

* [/order_list](https://shopping-website.herokuapp.com/order_list) ... Show all order history of all customer.
* [/dashboard](https://shopping-website.herokuapp.com/dashboard) ... Show charts for analysing purchase data.
* [/admin](https://shopping-website.herokuapp.com/admin) ... Add new data into database.

`All visitor` can see products but if visitor want to process purchase, sign up or login is needed.

`Customers` can add items into basket, complete an order, check own order history and profile.

`Staffs(Administrator)` can check all orders history and dashboard to manage this website.
Also, they can add new item and update exist item information by using Django default admin function.

## How to Start Server

Create `.env` file in root directory with below contents.

```.env
DEBUG=True
```

Then, start the server with this command.

```commandline
# install dependencies
pip install -r requirements.txt

# create database
python3 manage.py parse_csv

# create dummy data of customer and order
python3 manage.py create_dummy_data

# run server
python3 manage.py runserver 8000

# run server in Codio
python3 manage.py runserver 0.0.0.0:8000
```

## How to Run Tests
The tests were developed by `Behave`, `Selenium`, `Faker` and `Fixtures`.

### Behave Tests
Beahave tests are exist in `/featuers`.
There are <strong>23</strong> senarios and <strong>71</strong> steps tests developed by Behave.

Run by bellow command.
```commandline
bahave
```

### Form, Model, View Tests
Form, model, view tests are exist in `/tests`.
There are <strong>23</strong> form tests, <strong>10</strong> model tests, and <strong>32</strong> view tests.

Run by bellow command.
```commandline
python3 manage.py test
```

## Create User
You can create customer user from `/signup`.

If you want to create an superuser as staff of the shop, execute below command.

```commandline
python3 manage.py createsuperuser
```

Also, you can use user information which is already prepared.

* Superuser
    * username: `admin`
    * password: `P@ssw0rd`
* Customer user
    * username: `azusaw`
    * password: `P@ssw0rd`


## When Updated Code

If you change models, execute below command to make migration files and update database scheme.

```commandline
# create files for migration
python3 manage.py makemigrations

# execute migration
python3 manage.py migrate
```

If you add libraries, update `requirements.txt`.

```commandline
pip list --format=freeze > requirements.txt
```

## Data Source of Shopping Items

[Fashion Product Images Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)
by Kaggle.
