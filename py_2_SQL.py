import mysql.connector
import pandas as pd
import re


def main():
    # Retrieve our file, this one is current as of
    # August 24, 2020
    file = 'Budget.xlsx'
    df_dict = build_dataframes(file)

    # Find MySQL Server and connect
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='ratehufapacc',
        database='rdc'
    )

    # Create a cursor to interact with the MySQL Database
    c = mydb.cursor()

    # Now that we are connected to our MySQL database and
    # have our Excel data in a Pandas dataframe, we can start
    # automating the migration!

    # Note that our company's excel data does not have any
    # updating data for employees, business_connections,
    # or met_with

    update_customers(c, df_dict)


# This function returns a dictionary of pandas dataframes based
# on each sheet in our Excel file's name.
def build_dataframes(input_file):
    return pd.read_excel(input_file, sheet_name=['Inventory','Transactions','Costs',
                                                 'Anticipated Costs','Customer Requests','Margins'])

def update_orders(c, df_dict):
    df_transactions = df_dict['Transactions']


def update_customers(c, df_dict):
    # Checks for new customers in our database!
    # Check our pre-existing data
    c.execute('SELECT * FROM customers')

    # Use list comprehension to find the data
    # we currently have to build up a list of
    # current customers
    present_data = [row for row in c.fetchall()]
    current_customers = [(row[1] + row[2]).lower() for row in present_data]
    df_transactions = df_dict['Transactions']
    df_transactions = df_transactions.drop([0,1])

    # Add new customers to our database!
    for index, row in df_transactions.iterrows():
        name_list = row['Unnamed: 1'].split(' ')
        name_string = (name_list[0] + name_list[-1]).lower()
        if name_string not in current_customers:
            customer_id = "CU" + f"{(len(current_customers)+1):04d}"
            current_customers.append(name_string)
            customer_name = list(filter(None, row['Unnamed: 1'].split(' ')))
            first_name = customer_name[0]
            last_name = customer_name[-1]

            values = [customer_id, first_name, last_name]

            if pd.notnull(row['Unnamed: 2']):
                values.append(row['Unnamed: 2'])
            else:
                values.append("")
            if pd.notnull(row['Unnamed: 3']):
                values.append(row['Unnamed: 3'])
            else:
                values.append("")
            if pd.notnull(row['Unnamed: 4']):
                values.append(row['Unnamed: 4'])
            else:
                values.append("")
            values.append('') # User can specify preferences on request.

            insert_to_SQL(c, "customers", tuple(values))


def update_business_expenses(df_list):
    pass

def update_paid_for(df_list):
    pass

def update_sold_by(df_list):
    pass

def update_orders(df_list):
    pass

def update_employees(df_list):
    pass

def update_met_with(df_list):
    pass

def update_business_connections(df_list):
    pass

def update_products(c, df_dict):

    df_transactions = df_dict['Transactions']
    df_inventory = df_dict['Inventory']
    df_margins = df_dict['Margins']
    df_costs = df_dict['Costs']

    # Check our pre-existing data
    c.execute('SELECT * FROM products')

    # Use list comprehension to find the data
    # we currently have
    present_data = [row for row in c.fetchall()]

    # If no data exists, it is time to add new data!
    if len(present_data) == 0:

        # First, clean the data
        bad_labels = [df_inventory.columns[0]] + list(df_inventory.columns[5:])
        df_inventory = (df_inventory.drop(bad_labels, axis='columns'))
        col_names = list(df_inventory.iloc[1])
        df_inventory = df_inventory.drop([0,1])
        df_inventory.columns = col_names
        df_names = df_inventory['Producer'] + " " + df_inventory['Product Type']
        names_list = list(df_names.drop_duplicates())
        products = {}
        for name_value in range(len(names_list)):
            key = "PDCT" + f"{(name_value+1):04d}"
            products[key] = [names_list[name_value]]
            products[key] += []

        print(df_inventory)

    # If data DOES exist, we should only append new data
    else:
        highest_key = present_data[-1][0]

    return None

def insert_to_SQL(cursor, table_string, value):
    cmnd = "INSERT INTO products(customer_id, first_name, " \
           "last_name, contact_type, contact_info, " \
           "shipping_address, preferences)" \
           "VALUES (" + "%s,"*(len(value)-1) + "%s);"
    print(cmnd)
    cursor.execute(cmnd, value)

main()


# Accomplished with reference to
# https://www.youtube.com/watch?v=71zkSuzkJrw (pandas file extraction)
# https://www.w3schools.com/python/python_mysql_getstarted.asp (connection to mySQL database)
# https://stackoverflow.com/questions/11339210/how-to-get-integer-values-from-a-string-in-python (extracting integers from strings using re)
# https://stackoverflow.com/questions/134934/display-number-with-leading-zeros (Placing leading zeros in a number)
# https://www.youtube.com/watch?v=kJkNRbKzs6w (How to concatenate dataframe strings)