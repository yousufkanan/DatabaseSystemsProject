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
    CREATE TABLE Events (
        EventName VARCHAR(255) NOT NULL,
        Date DATE NOT NULL,
        Result VARCHAR(255) NOT NULL,
        Fighter1 VARCHAR(255) NOT NULL,
        Fighter2 VARCHAR(255) NOT NULL,
        KnockDowns1 INT,
        KnockDowns2 INT,
        Srikes1 INT,
        Srikes2 INT ,
        Takedowns1 INT ,
        Takedowns2 INT ,
        SubmissionAttempts1 INT ,
        SubmissionAttempts2 INT,
        WeighClass VARCHAR(255) NOT NULL,
        Method VARCHAR(255) NOT NULL,
        Round INT NOT NULL,
        Time TIME NOT NULL

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
    file = open('archive/ufc_event_data.csv', 'r')
    #Print each row in the csv file
    reader = csv.reader(file)
    next(reader) # skip the header row
    id = 0
    for row in reader:
        date = convertDate(row[1])
        if row[5] == "-----":
            knockdown = ["NULL", "NULL"]
        else:
            knockdown = row[5].split("-")
        if row[7] == "-----":
            takedown = ["NULL", "NULL"]
        else:
            
            takedown = row[7].split("-")
        if row[6] == "-----":
            strike = ["NULL", "NULL"]
        else:
            strike = row[6].split("-")
        if row[8] == "-----":
            submission = ["NULL", "NULL"]
        else:
            submission = row[8].split("-")

        sql = f'Insert INTO Events (EventName, Date, Result, Fighter1, Fighter2, KnockDowns1, KnockDowns2, Srikes1, Srikes2, Takedowns1, Takedowns2, SubmissionAttempts1, SubmissionAttempts2, WeighClass, Method, Round, Time) \
            VALUES ("{row[0]}", "{date}", "{row[2]}", "{row[3]}", "{row[4]}", {knockdown[0]}, {knockdown[1]}, {strike[0]}, {strike[1]}, {takedown[0]}, {takedown[1]}, {submission[0]}, {submission[1]}, "{row[9]}", "{row[10]}", "{row[11]}", "{row[12]}");'

        id += 1
        try: 
            cursor.execute(sql)
        # except mysql.connector.Error as err:
        #     print(f"Error: {err}")
        #     print(sql)
        #     exit(1)
        except:
            print("Error")
            print(sql)
            exit(1)
        # print(id)
    file.close()
    print("Fighter table populated")
    print(sql)

def convertDate(date):
    #Date is in "November 04, 2023" format
    #Convert to "2023-11-04" format
    date = date.split(" ")
    month = date[0]
    day = date[1].replace(",", "")
    year = date[2]
    if month == "January":
        month = "01"
    elif month == "February":
        month = "02"
    elif month == "March":
        month = "03"
    elif month == "April":
        month = "04"
    elif month == "May":
        month = "05"
    elif month == "June":
        month = "06"
    elif month == "July":
        month = "07"
    elif month == "August":
        month = "08"
    elif month == "September":
        month = "09"
    elif month == "October":
        month = "10"
    elif month == "November":
        month = "11"
    elif month == "December":
        month = "12"

    return year + "-" + month + "-" + day    

def main():
    DB_NAME = 'finalProject'
    cursor, connection = connectToMySQL()
 #   createDatabase(cursor, DB_NAME)  # comment this line after first successful run
    cursor.execute("USE {}".format(DB_NAME))
   # makeTable(cursor)   # comment this line after first successful run
    insertData(cursor)  # comment this line after first successful run

    # don't modify below this line
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
