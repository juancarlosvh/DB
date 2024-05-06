import mysql.connector

class DBConnect():

	Host_Name = ""
	User_Name = ""
	Password  = ""
	Database_Name =""

	def __init__( self,Host_Name,User_Name,Password,Database_Name):
		self.Host_Name = Host_Name
		self.User_Name = User_Name
		self.Password  = Password
		self.Database_Name =Database_Name

	def connectiondb(self):
		try:
			self.connection = mysql.connector.connect(host=self.Host_Name,user=self.User_Name,password=self.Password,database=self.Database_Name)
			self.cursor = self.connection.cursor()
			return True
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
			self.connectiondb()

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