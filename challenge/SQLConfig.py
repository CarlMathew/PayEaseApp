import mysql.connector
from mysql.connector import Error


class APPSQL:
    def __init__(self, database):
        self.username = 'sql12735044'
        self.hostname = 'sql12.freesqldatabase.com'
        self.password = 'CY1bvbWVQf'
        self.dbname = database
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host = self.hostname,
                user = self.username,
                passwd = self.password,
                db = self.dbname)
            print("Connected Successfully")
        except Error as err:
            print(f"Error as: {err}")
    def read_database(self, query):
        cursor = self.connection.cursor(dictionary=True)
        results = []
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as err:
            print(f"Error as: {err}")
    def update_database(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except Error as err:
            print(f"Error: {err}")

if __name__ =="__main__":
    connection = APPSQL('sql12735044')
    query1 = 'UPDATE TestTable SET Name = "Carl" WHERE ID = 1'
    results = connection.update_database(query1)
    print(results)
    connection.connection.close()
    
            
        
        
        