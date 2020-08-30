import mysql.connector
import pandas as pd


def main():
    # Retrieve our file, this one is current as of
    # August 24, 2020
    file = 'Budget.xlsx'
    df_dict = build_dataframes(file)

    # Find MySQL Server and connect
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
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

    update_customers(mydb, c, df_dict)
    update_business_expenses(mydb, c, df_dict)
    update_orders(mydb, c, df_dict)


# This function returns a dictionary of pandas dataframes based
# on each sheet in our Excel file's name.
def build_dataframes(input_file):
    return pd.read_excel(input_file, sheet_name=['Inventory','Transactions','Costs',
                                                 'Anticipated Costs','Customer Requests','Margins'])

# Checks for new customers to add to our SQL database
def update_customers(mydb, c, df_dict):
    # Check our pre-existing data
    c.execute('SELECT * FROM customers')

    # Use list comprehension to show us which
    # customers are already in our SQL database
    present_data = [row for row in c.fetchall()]
    current_customers = [(row[1] + row[2]).lower() for row in present_data]

    # Extract valuable information from the
    # 'Transactions' page of our SQL database
    df_transactions = df_dict['Transactions']
    df_transactions = df_transactions.drop([0,1])

    # Add new customers to our database!
    new_customers = []
    for index, row in df_transactions.iterrows():
        customer_name_list = list(filter(None, row['Unnamed: 1'].split(' ')))
        name_string = (customer_name_list[0] + customer_name_list[-1]).lower()
        if name_string not in current_customers:
            next_highest_key = int(present_data[-1][0][2:]) + 1
            customer_id = 'CU' + f'{next_highest_key:04d}'
            current_customers.append(name_string)

            first_name = customer_name_list[0]
            last_name = customer_name_list[-1]

            values = [customer_id, first_name, last_name]

            if pd.notnull(row['Unnamed: 2']):
                values.append(row['Unnamed: 2'])
            else:
                values.append(None)
            if pd.notnull(row['Unnamed: 3']):
                values.append(row['Unnamed: 3'])
            else:
                values.append(None)
            if pd.notnull(row['Unnamed: 4']):
                values.append(row['Unnamed: 4'])
            else:
                values.append(None)
            values.append(None) # User can specify preferences on request.
            new_customers.append(tuple(values))

    insert_to_SQL(mydb, c, 'customers', new_customers)

# Checks for new business_expenses to add to our SQL database
def update_business_expenses(mydb, c, df_dict):
    # Check our pre-existing SQL database to
    # see if entries are already there
    c.execute('SELECT * FROM business_expenses')
    present_data = [row for row in c.fetchall()]

    current_expenses = [(str(row[4]) + row[1] + row[2]).lower()
                        for row in present_data]

    # Gather and clean data from our Excel Spreadsheet
    df_expenses = df_dict['Costs']
    df_expenses = (df_expenses.drop([0,1]))
    df_expenses.columns = ['DatePurchased', 'Supplier', 'ItemName',
                           'ItemPrice', 'ItemQuantity', 'ItemSize',
                           'ShippingCost', 'PPU', 'TotalCost', 'Notes']

    # Add new data to our SQL database from our Excel Spreadsheet
    new_expenses = []
    for index, row in df_expenses.iterrows():
        expense_tag = (str(row['DatePurchased'].date()) + row['Supplier'] + row['ItemName']
                       ).lower()

        if expense_tag not in current_expenses:
            next_highest_key = int(present_data[-1][0][3:]) + 1
            expense_id = 'EXP' + f'{next_highest_key:04d}'
            current_expenses.append(expense_tag)
            expense = [expense_id, row['Supplier'], row['ItemName'],
                       row['TotalCost'], str(row['DatePurchased'].date()), None]

            new_expenses.append(tuple(expense))

    insert_to_SQL(mydb, c, 'business_expenses', new_expenses)

# Scans the Excel spreadsheet and looks for new
# Orders to add to our SQL database
def update_orders(mydb, c, df_dict):
    c.execute('SELECT * FROM orders')
    present_data = [row for row in c.fetchall()]
    #               customer_id + product_id + date
    current_orders = [(row[1] + row[2] + str(row[3])).lower()
                      for row in present_data]

    # Our orders table will be more complicated. The Orders table will require
    # information from other SQL tables and multiple Excel sheets.

    df_transactions = df_dict['Transactions']
    df_transactions = df_transactions.drop([0, 1])



    new_orders = []
    for index, row in df_transactions.iterrows():
        # Retrieve Customer ID
        customer_names = list(filter(None, row['Unnamed: 1'].split(' ')))
        cmnd = ('SELECT * FROM customers ' \
                  "WHERE customers.first_name=%s " \
                  "AND customers.last_name=%s")
        c.execute(cmnd, (customer_names[0], customer_names[-1]))
        customer_id = c.fetchone()[0]

        #Retrieve Product ID
        product_name = row['Unnamed: 7'].replace('Coffee', '')
        cmnd = ('SELECT * FROM products ' \
                "WHERE products.product_name='" + product_name + "'")
        c.execute(cmnd, product_name)
        product_info = c.fetchone()

        if product_info is None:
            print("\nOrder for customer ",customer_id, "on",
                  row['Transactions'].date(),"needs review,")
            print('Product: "' + product_name + '" not found.\n')
        else:
            product_id = product_info[0]

            #Retrieve Order Date
            order_date = row['Transactions'].date()

            # Find the key for this order
            if len(present_data) == 0:
                next_highest_key = 1
            else:
                next_highest_key = int(present_data[-1][0][3:]) + 1

            order_tag = (customer_id + product_id + str(order_date)).lower()
            if order_tag not in current_orders:

                if len(present_data) == 0:
                    order_id = 'ORD' + f'{(len(current_orders)+1):04d}'
                else:
                    order_id = 'ORD' + f'{next_highest_key:04d}'
                current_orders.append(order_tag)
                order = (order_id, customer_id, product_id,
                        order_date, product_name, row['Unnamed: 6'],
                        row['Unnamed: 13'], row['Unnamed: 8'],
                        row['Unnamed: 8'] * 0.065, # Calculate sales tax
                        0.00, None, None)

                new_orders.append(tuple(order))

    insert_to_SQL(mydb, c, 'orders', new_orders)


# This function takes a list of tuples and inserts them
# directly into the RDC SQL database
def insert_to_SQL(mydb, cursor, table_name, values):
    if len(values) == 0:
        print("No new " + table_name + ".")
    else:
        cmnd = "INSERT INTO " + table_name + " " \
                "VALUES (" + "%s,"*(len(values[0])-1) + "%s);"
        cursor.executemany(cmnd, values)

        #mydb.commit()

        print(cursor.rowcount, "new rows added to " + table_name + ".")

main()


# Accomplished with reference to:

# https://www.youtube.com/watch?v=71zkSuzkJrw (pandas file extraction)
# https://www.w3schools.com/python/python_mysql_getstarted.asp (connection to mySQL database)
# https://stackoverflow.com/questions/11339210/how-to-get-integer-values-from-a-string-in-python (extracting integers from strings using re)
# https://stackoverflow.com/questions/134934/display-number-with-leading-zeros (Placing leading zeros in a number)
# https://www.youtube.com/watch?v=kJkNRbKzs6w (How to concatenate dataframe strings)
# https://mysql.az/tag/error-1054-42s22-unknown-column-in-field-list/ Used to fix error 1054, single quotes are required for all strings!