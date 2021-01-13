import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]

order_management_db = myclient["order_management"]

products = {
100: {"name":"Americano","price":125},
200: {"name":"Brewed Coffee","price":110},
300: {"name":"Cappuccino","price":120},
400: {"name":"Espresso","price":120},
500: {"name":"Latte","price":140},
600: {"name":"Cold Brew","price":200}
}

branches = {
1: {"name":"Katipunan"},
2: {"name":"Tomas Morato"},
3: {"name":"Eastwood"},
4: {"name":"Tiendesitas"},
5: {"name":"Arcovia"},
}

users = {
    "chums@example.com":{"password":"Ch@ng3m3!",
                         "first_name":"Matthew",
                         "last_name":"Uy"},
    "joben@example.com":{"password":"Ch@ng3m3!",
                         "first_name":"Joben",
                         "last_name":"Ilagan"},
    "bong@example.com":{"password":"Ch@ng3m3!",
                        "first_name":"Bong",
                        "last_name":"Olpoc"},
    "joaqs@example.com":{"password":"Ch@ng3m3!",
                         "first_name":"Joaqs",
                         "last_name":"Gonzales"},
    "gihoe@example.com":{"password":"Ch@ng3m3!",
                         "first_name":"Gio",
                         "last_name":"Hernandez"},
    "vic@example.com":{"password":"Ch@ng3m3!",
                       "first_name":"Vic",
                       "last_name":"Reventar"},
    "joe@example.com":{"password":"Ch@ng3m3!",
                       "first_name":"Joe",
                       "last_name":"Ilagan"},
}

def get_user(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user


def get_product(code):
    products_coll = products_db["products"]
    product = products_coll.find_one({"code":code})
    return product

def get_products():
    product_list = []
    products_coll = products_db["products"]
    for p in products_coll.find({}):
        product_list.append(p)

    return product_list

# def get_user(username):
#     try:
#        return users[username]
#     except KeyError:
#         return None

def get_branch(code):
    branches_coll = products_db["branches"]
    branch = branches_coll.find_one({"code":code})
    return branch


def get_branches():
    branch_list = []
    branches_coll = products_db["branches"]
    for b in branches_coll.find({}):
        branch_list.append(b)

def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)

def get_orders(username):
    orders_coll = order_management_db['orders']
    orders = orders_coll.find({"username":username})
    return orders

