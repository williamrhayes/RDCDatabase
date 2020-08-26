# RDCDatabase
Learning how to design a relational database for my company!

---------------------------------------------------------------
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
Step 1: Drafting a Database Design
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 

For this project, I am heavily referencing Malcom Hamer's book
"Relational Database Practices: Bridging the Gap Between the
Theory of Database Design and Real-World Practices." as well
as my Mike Dane's introduction to SQL course, available at
https://www.youtube.com/watch?v=HXV3zeQKqGY

After consulting these two references, I attempted to draft
a database that could remain "normalized". A normalized 
database is one where inserting and deleting data does not
cause harm to the valuable information within the database.

To begin, I sketched out an entity-relationship diagram.
The result is the file titled:  

"RDC_Database_Design_Rough_Sketch.pdf"

Of course, this was hardly legible. Therefore, I uploaded

"RDC_ER_Diagram.pdf"

to display the information in a nicer format. In this PDF
file, entities are light blue squares, relationships are
orange diamonds, and attributes are deep blue ovals.

First, I have laid out all the important entities of my business
that I could think of. This included

employees,
products,
customers,
business_expenses, and
business_connections.

Then, I thought about how they would relate to one another. 
For instance

a customer orders a product,

so an "orders" table would need to be constructed to keep track
of which customers ordered which products. I connected my entities
with relationships called

orders,
sold_by,
met_with, and
paid_for.


Finally, I added attributes to these tables. Attributes 
are the fields that describe our entities or relationships. 
More importantly, this is where the data is entered!
These include fields such as

a customer's name, 
the price of a product, or
the contact information of a business connection.

some instances for an entity like an employee are the 
employee's 

title,
join_date,
first_name, and
employee_id.

Here, employee_id serves as the primary key for the "employee"
entity. This key is the unique identifier for each person
in our company. When it is referenced, it should be able to
bring up data associated with that specific person.

In some cases you will see "aiwt" tagged at the end of some of
these attributes. This stands for "as it was then" and 
takes after Malcom Hamer's technique of specifying that the data
is historical (and therefore immutable). This prevents, say, 
an item from the "products" table from changing its price and 
subsequently altering the price of that product in the past order 
information! 



---------------------------------------------------------------
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
Step 2: Generating a Database Catalog
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 

The next step is kind of like flossing. It was mentioned as a
good practice by Hamer so I figured I would give it a shot.

The database catalog,

"DB_Catalog.xlsx"

specifies the data type of each attribute, whether that 
attribute is constrained (FALSE if it can accept NULL values), 
and gives an example of an entry for the table. 

---------------------------------------------------------------
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
Step 3: Implementing this Database Design in SQL
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 

I had already tested out building a toy database before so 
establishing a new database for the company was relatively
easy. All I had to do was establish a new database with the 
MySQL command client (which I appropriately named 'rdc'), then
use PopSQL to implement my SQL code!

As I was creating tables in MySQL I found the database
catalog pretty handy. I could just reference the catalog 
as I was filling out information types. While I was doing this
I found out that the "MONEY" data type was only available in
Transact-SQL, so I decided to use the DECIMAL data type instead.
From what I understand, this data type is perfectly safe to use
with money (unlike floats).

Once I had corrected all the typos and squared away all the 
variable names, I inserted myself and my business partner into
our database! I wasn't sure if there was a SQL-specific file
format, so all code used to construct the database can be 
found in the 

"RDC_SQL_Commands.txt" 

file.

Next we need to migrate our company's excel data to our MySQL 
server. Hopefully we can accomplish this in a way that can
automate SQL commands for future reports.

---------------------------------------------------------------
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
Step 4: Migrating data from Excel to our SQL server
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 

This is definetly going to be the hardest part of establishing 
our new database.

I had to decide which parts of the information from our Excel
sheet I wanted to automate and which could be manually inserted. 
While I initially tried to automate the update of each individual 
table, I found that some tables (such as products) were easier to
just add to directly in SQL. I tried setting up an automated system 
for keeping track of products, but this was just too much effort to
keep track of 7 different products.

I decided that creating our customer database would drastically
benefit from automation, and found out that we have about ~70 total
unique customers. My updates will be featured in the

"py_2_SQL.py"

Python script!

---------------------------------------------------------------
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
Step 5: Maintaining our SQL database
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
