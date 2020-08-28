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

    update_customers(mydb, c, df_dict)
    update_business_expenses(mydb, c, df_dict)


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
            customer_id = 'CU' + f'{(len(current_customers)+1):04d}'
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
            expense_id = 'EXP' + f'{(len(current_expenses)+1):04d}'
            current_expenses.append(expense_tag)
            expense = [expense_id, row['Supplier'], row['ItemName'],
                       row['TotalCost'], str(row['DatePurchased'].date()), None]

            new_expenses.append(tuple(expense))

    insert_to_SQL(mydb, c, 'business_expenses', new_expenses)


def update_orders(mydb, c, df_dict):
    pass


# This function takes a list of tuples and inserts them
# directly into the RDC SQL database
def insert_to_SQL(mydb, cursor, table_name, values):
    if len(values) == 0:
        print("No new " + table_name + ".")
    else:
        cmnd = "INSERT INTO " + table_name + " " \
                "VALUES (" + "%s,"*(len(values[0])-1) + "%s);"
        cursor.executemany(cmnd, values)
        mydb.commit()
        print(cursor.rowcount, "new rows added to " + table_name + ".")


main()


# Accomplished with reference to:

# https://www.youtube.com/watch?v=71zkSuzkJrw (pandas file extraction)
# https://www.w3schools.com/python/python_mysql_getstarted.asp (connection to mySQL database)
# https://stackoverflow.com/questions/11339210/how-to-get-integer-values-from-a-string-in-python (extracting integers from strings using re)
# https://stackoverflow.com/questions/134934/display-number-with-leading-zeros (Placing leading zeros in a number)
# https://www.youtube.com/watch?v=kJkNRbKzs6w (How to concatenate dataframe strings)
# https://mysql.az/tag/error-1054-42s22-unknown-column-in-field-list/ Used to fix error 1054, single quotes are required for all strings!