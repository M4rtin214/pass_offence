# scritps for returns value of passage/offence 
# version: Python 2.7
# arguments: ID section, p/o (passage/offence), time(only passage)


import sys
import pyodbc
import datetime


# connection to db
def conn_to_db():
    try:
        connDB = pyodbc.connect('DRIVER={SQL Server};SERVER=VIRTUALNO2\SQLEXPRESS2012;Trusted_Connection=yes;')
        connDB.autocommit = True
        cursor = connDB.cursor()
        return cursor
    except:
        error = "Database connection error! "
        print (error)
        sys.exit(1)

# get utc time
def utc_time():
    now = datetime.datetime.utcnow()  
    now = str(now)
    now = now[0:10]
    return now

# returns value of passage at the entered time
def countPassages(sectionID, timeFrom, timeTo):
    try:
        cursor = conn_to_db()
        cursor.execute("""SELECT COUNT([Id])
        FROM [RedCon].[dbo].[PassageCarSet] WHERE Date BETWEEN '""" + str(timeFrom) + """' AND '""" + str(timeTo) + """' AND SuId = '""" + sectionID + """'
                        """)
        passage = cursor.fetchone()
        passage = passage[0]
        passage = str(passage)
        return passage
    except:
        passage = "error"
        return passage

# returns today value of offences
def countOffence(sectionID, nowDate):
    try:
        cursor = conn_to_db()
        cursor.execute("""
            SELECT COUNT([OffenceId])
        FROM [RedCon].[dbo].[OffenceLogSet] WHERE Date > '""" + nowDate + """' AND SuId = '""" + sectionID + """'
                        """)
        offence = cursor.fetchone() #return list
        offence = offence[0] #first value of list
        offence = str(offence)
        return offence
    except:
        offence = "error"
        return offence


# main
if __name__ == "__main__":
    try:
        func = sys.argv[2][0]
        func = str(func)
        sectionID = str(sys.argv[1])
        sectionID = sectionID.upper()
    except:
        print("Unknown parameter!")
        sys.exit(1)

    if func == "p":
        timeShift = int(sys.argv[3])
        timeFrom = datetime.datetime.utcnow() - datetime.timedelta(minutes=timeShift)
        timeFrom = timeFrom.strftime('%Y-%m-%d %H:%M:%S')
        timeFrom = timeFrom.lstrip('0')
        timeTo = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        passage = countPassages(sectionID, timeFrom, timeTo)
        sys.stdout.write(passage)
        sys.exit(0)
    elif func == "o":
        nowDate = utc_time()
        offence = countOffence(sectionID, nowDate)
        sys.stdout.write(offence)
        sys.exit(0)
    else:
        print("Unknown parameter!")
        sys.exit(1)


