# RDCDatabase
Learning how to design a relational database for my company!

---------------------------------------------------------------
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
Step 1: Drafting a Database Design (Formally Database Schema)
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
The result is my first initial sketch titled:  
"RDC_Database_Design_Rough_Sketch.pdf"

First, I have laid out all the important entities of my business
that I could think of. This included

employees,
products,
customers,
business_expenses, and
business_connections.

Then, I thought about how they would relate to one another. 
For instance, 

customer orders product,

so an "orders" table would need to be constructed to keep track
of 

---------------------------------------------------------------
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
Step 2: Generating a Database Catalog
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
---------------------------------------------------------------
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
Step 3: Implementing this Database Design in SQL
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
---------------------------------------------------------------
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
Step 4: Migrating data from Excel to our SQL server
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
---------------------------------------------------------------
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
Step 5: Maintaining our SQL database
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
