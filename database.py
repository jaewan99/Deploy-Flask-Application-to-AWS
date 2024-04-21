import pymongo
from flask import session


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
products_db = myclient["products"]
order_management_db = myclient["order_management"]

def get_product(code):
    products_coll = products_db["products"]
    product = products_coll.find_one({"code":code}, {"_id":0})
    return product


def get_products():
    product_list = []
    products_coll = products_db["products"]
    for p in products_coll.find({},{"_id":0}):
        product_list.append(p)
    return product_list

def api_get_product(code):
    products_coll = products_db["products"]
    product = products_coll.find_one({"code":code}, {"_id":0})
    return product


def get_branch(code):
    branches_coll = products_db["branches"]
    branch = branches_coll.find_one({"code":code})
    return branch

def get_branches():
    branch_list = []
    branches_coll = products_db["branches"]
    for b in branches_coll.find({}):
        branch_list.append(b)
    return branch_list

def get_user(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user


def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert_one(order)

def get_user_orders():
    order_list = []
    orders_coll = order_management_db["orders"]
    for o in orders_coll.find({}):
        if (o["username"]) == (session["user"]["username"]):
            order_list.append(o)
    return order_list

def get_user_password(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user["password"]

def change_user_password(pwd):
    customers_coll = order_management_db['customers']
    customers_coll.update_one({"username":session["user"]["username"]}, {"$set": {"password": pwd}})




# users = {
#     "chums@example.com":{"password":"Ch@ng3m3!",
#                          "first_name":"Matthew",
#                          "last_name":"Uy"},
#     "joben@example.com":{"password":"Ch@ng3m3!",
#                          "first_name":"Joben",
#                          "last_name":"Ilagan"},
#     "bong@example.com":{"password":"Ch@ng3m3!",
#                         "first_name":"Bong",
#                         "last_name":"Olpoc"},
#     "joaqs@example.com":{"password":"Ch@ng3m3!",
#                          "first_name":"Joaqs",
#                          "last_name":"Gonzales"},
#     "gihoe@example.com":{"password":"Ch@ng3m3!",
#                          "first_name":"Gio",
#                          "last_name":"Hernandez"},
#     "vic@example.com":{"password":"Ch@ng3m3!",
#                        "first_name":"Vic",
#                        "last_name":"Reventar"},
#     "joe@example.com":{"password":"Ch@ng3m3!",
#                        "first_name":"Joe",
#                        "last_name":"Ilagan"},
# }
# products = {
#     100: {"name":"Americano","price":125},
#     200: {"name":"Brewed Coffee","price":100},
#     300: {"name":"Cappuccino","price":120},
#     400: {"name":"Espresso","price":120},
#     500: {"name":"Latte", "price":140},
#     600: {"name":"Cold Brew", "price":200},
#     1000: {"name":"Tiramisu", "price":150},
#     1100: {"name":"Red Velvet", "price":130},
#     1200: {"name":"Mango Cream Pie", "price":200}
# }
# branches = {
#     1: {"name":"Katipunan","phonenumber":"09179990000"},
#     2: {"name":"Tomas Morato","phonenumber":"09179990001"},
#     3: {"name":"Eastwood","phonenumber":"09179990002"},
#     4: {"name":"Tiendesitas","phonenumber":"09179990003"},
#     5: {"name":"Arcovia","phonenumber":"09179990004"},
# }