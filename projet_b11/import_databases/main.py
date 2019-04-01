import mysql.connector
from ThreeDid import *

# init mysql connection
try:
    db_connection = mysql.connector.connect(user='root', host='localhost')
    db_cursor = db_connection.cursor()
except mysql.connector.Error as e:
    print(e)

did = ThreeDid()

# did.fetch_version()
# print(did.version)

# did.download_archive():
# did.extract_archive():
# did.import_sql(db_cursor):

did.print_ddi(db_cursor)

db_connection.close()
db_cursor.close()
