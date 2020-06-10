'''
table = collection.
row = document.
column = field.
Database = database
index = index
'''
import csv
# import logging
from pymongo import MongoClient
from pprint import pprint

class MongoDBConnection(object):
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(directory_name,  product_file,  customer_file,  rentals_file):
    '''This function takes a directory name three csv files as input,  one with
product data,  one with customer data and the third one with rentals data and
creates and populates a new MongoDB database with these data. It returns 2
tuples:  the first with a record count of the number of products,  customers
rentals added (in that order),  the second with a count of any errors that
occurred,  in the same order.'''
    product_file_uploads = 0

    mongo = MongoDBConnection()
    # why does this need a 'with'
    with mongo:
        # creating the DB
        db = mongo.connection.norton
        # creating the tables/collections
        product_file_table = db['products']
        customer_file_table = db['customers']
        rentals_file_table = db['rentals']
        # db.products.drop() # why won't it work with the alias?
        # db.customers.drop() # why won't it work with the alias?
        # db.rentals.drop() # why won't it work with the alias?

    with open(f'{directory_name}/{product_file}', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # how do I set the ID?
            product_file_table.insert_one(row)
            product_file_uploads += 1

    print(product_file_uploads)

    cursor = product_file_table.find({})
    for document in cursor:
        pprint(document)


def show_available_products():
    ''' Returns a Python dictionary of products listed as available
-product_id.
-description.
-product_type.
-quantity_available.'''


{'prd001': {'description': '60-inch TV stand', 'product_type': 'livingroom', 'quantity_available': '3'}
, 'prd002': {'description': 'L-shaped sofa', 'product_type': 'livingroom', 'quantity_available': '1'}}


def show_rentals(product_id):
    '''Returns a Python dictionary with the following user information from
users that have rented products matching product_id:
-user_id.
-name.
-address.
-phone_number.```
-email.'''


{'user001': {'name': 'Elisa Miles', 'address': '4490 Union Street',
             'phone_number': '206-922-0882', 'email': 'elisa.miles@yahoo.com'}
, 'user002': {'name': 'Maya Data', 'address': '4936 Elliot Avenue',
'phone_number': '206-777-1927', 'email': 'mdata@uw.edu'}}
