import mysql.connector

class DBConnect():

	def __init__( self ):
		pass

	def connection(self,Host_Name,User_Name,Password,Database_Name):
		try:
			self.connection = mysql.connector.connect(host=Host_Name,user=User_Name,password=Password,database=Database_Name)
			self.cursor = self.connection.cursor()
			return self.cursor
		except mysql.connector.Error as e:
			return e
		
	def close(self):
		self.connection.close()
		self.cursor.close()

	def execute_sql(self, sql, database):
		try:
			self.connection()

			self.cursor.execute(sql)
			result = self.connection.commit()
			self.close()
			return result
		except mysql.connector.Error as e:
			return e
	
	def return_data(self,sql,database=''):
		try:
			self.connection()

			self.cursor.execute(sql)
			data = self.cursor.fetchall()
			
			self.close()
			return data
		except mysql.connector.Error as e:
			return e
"""
e = DBConnect()
print(e.return_data("SHOW SCHEMAS",""))
"""