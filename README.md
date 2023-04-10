# shopping-website

## Heroku URL

https://shopping-website.herokuapp.com/

## Description

This website is developed with Django.
The requirement was creation of shopping website, so I chose the data which has image data because it makes good view
for visitor.
The theme of website is "apareru items", 様々なブランドのアイテムを横断して注文することが可能なアパレルポータルです。

This website has a lot of pages, access permission is managed by user role of login user.

### For All User

* [/](https://shopping-website.herokuapp.com/) ... All product list.
* [/detail/<item_id>'](https://shopping-website.herokuapp.com/detail/???) ... Product detail and add to cart.
* [/signup'](https://shopping-website.herokuapp.com/signup) ... Sign up customer user.
* [/signin'](https://shopping-website.herokuapp.com/signin) ... Sign in by username and password.

### For Customer User

* [/profile](https://shopping-website.herokuapp.com/profile) ... Customer can update user profile.
* [/order_list](https://shopping-website.herokuapp.com/order_list) ... All order history of login customer.
* [/order/<order_id>](https://shopping-website.herokuapp.com/order/???) ... Order detail of selected order.
* [/thanks/<order_id>](https://shopping-website.herokuapp.com/thanks/???) ... Thanks page for order.
* [/basket](https://shopping-website.herokuapp.com/basket) ... Check current basket and proceed purchase.
* [/purchase](https://shopping-website.herokuapp.com/purchase) ... Process purchase.
* [/payment](https://shopping-website.herokuapp.com/payment) ... Input payment information to complete an order.

### For Staff User

* [/order_list](https://shopping-website.herokuapp.com/order_list) ... All order history of all customer.
* [/dashboard](https://shopping-website.herokuapp.com/dashboard) ... Charts for analysing purchase data.
* [/admin](https://shopping-website.herokuapp.com/admin/??) ... Add new data into database.

All visitor can see products but if visitor want to add to basket, sign up or login is needed.
Customers can add items into basket, complete an order, check own order history.
Staff users can check all orders history and dashboard to manage this website.
Also, they can add new item and update exist item information by using Django default admin function.

## Data Source of Shopping Items

[???](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)
by Kaggle.

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

# run server
python3 manage.py runserver 8000

# run server in Codio
python3 manage.py runserver 0.0.0.0:8000
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

## How to Run Tests

The tests were developed by xxx.

```commandline
python3 manage.py test
```

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