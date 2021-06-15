import pymysql

mydb = pymysql.connect(
    host="mysql-32671-0.cloudclusters.net",
    user="student",
    passwd="benq1234",
    port=32671,
    database="DiplomBase"
)
mycursor = mydb.cursor()



