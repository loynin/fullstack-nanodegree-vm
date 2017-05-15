Swiss Tournament Project
------------------------

Content

1. Project Description
2. Structure of Project Files
3. How to Run the Project


1. Project Description:
-----------------------

The purpose of this project is to use PostgreSQL database to keep 
track of players and matches during a game in the tournament, and 
then use Python module to rank the players and pair them up in matches
in a tournament.

2. Structure of Project Files
-----------------------------

There are four files in this project, and they are: tournament.sql,
tournament.py, tournament_test.py, and readme.txt. 

   a. tournament.sql is used to store the information about database
      schema, in the form of SQL commands. It used create database and
      create table commands to create database and table for the project.
   b. tournament.py is used to store the code of the Python module. There are 
      several functions used to process the purpose of the project.
   c. tournament_test.py contains unit tests that will test the function that 
      were written in tournament.py
   d. readme.txt is this file. Use to describe the project description and
      instruction of how to run the project.
      
3. How to Run the Project
-------------------------

Before running the code or create the tables, there will be a need to create 
database first. In this project, follow these steps in order to successfully 
run the code of the project:
   
   a. Create database and tables from the statements in tournament.sql
      There are two ways to do this:
         - Paste each statement into psql
         - Use the commnad \i tournament.sql to import the whole file into 
           psql at once.
   b. Run the project by using command:
      python tournament_test.py
      
      If the program run correctly, it will show the result of the last line,
      "Success! All tests pass!"
      
      