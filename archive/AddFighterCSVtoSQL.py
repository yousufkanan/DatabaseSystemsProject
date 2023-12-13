"""
Will Create two tables in the database
    1. Table from the ufc_fighters.csv file
    2. Table from the ufc_fights.csv file

CLASS: DATABSE SYSTEMS

INSTRUCTOR: DR. GREGORY SCHAPER

AUTHOR: YOUSUF KANAN AND DEREK Allmon 
"""

import csv 
import mysql.connector 

# Connect to the database
def connectToMySQL():
    cnx = mysql.connector.connect(password = 'project', user='project')
    cursor = cnx.cursor()
    return cursor, cnx

def createDatabase(cursor, DB_NAME):
    '''
    :param cursor: instance of the connection to the database
    :param DB_NAME: name of the database to create
    Creates the database at cursor with the given name.
    '''
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)



def makeTable(cursor):
    sql = """
    CREATE TABLE Fighter (
        id INT PRIMARY KEY,
        firstName VARCHAR(30),
        lastName  VARCHAR(30),
        nickName VARCHAR(30),
        Height FLOAT,
        Weight FLOAT,
        REACH FLOAT,
        STANCE VARCHAR(30),
        WINS INT,
        LOSSES INT,
        DRAWS INT
    );
    """
    try:
        cursor.execute(sql)
        print("Fighter table created")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if err.errno == 1050:  # Error code for "Table already exists"
            print("The table 'Fighter' already exists.")
        else:
            print("Failed to create the table.")

     #   print(new_row[1].split('"'))
def insertData(cursor):
    file = open('archive/AlteredFightersData.csv', 'r')
    #Print each row in the csv file
    reader = csv.reader(file)
    next(reader) # skip the header row
    id = 0
    for row in reader:
        if row[5] == 'NULL':
            reach = 'NULL'
        else:
            reach = row[5][:-1]
        sql = f"INSERT INTO Fighter (id, firstName, lastName, nickName  ,Height, Weight, REACH, STANCE, WINS, LOSSES, DRAWS) \
        VALUES ({id}, \"{row[0]}\", \"{row[1]}\", \"{row[2]}\", {row[3]}, {row[4]}, {reach}, '{row[6]}', {row[7]}, {row[8]}, {row[9]});"


        id += 1
        try: 
            cursor.execute(sql)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            print(sql)
            exit(1)
        # print(id)
    file.close()
    print("Fighter table populated")
    print(sql)




def main():
    DB_NAME = 'finalProject'
    cursor, connection = connectToMySQL()
 #   createDatabase(cursor, DB_NAME)  # comment this line after first successful run
    cursor.execute("USE {}".format(DB_NAME))
    makeTable(cursor)   # comment this line after first successful run
    insertData(cursor)  # comment this line after first successful run

    # don't modify below this line
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
