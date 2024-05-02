from dbConnect import DBConnect
from config import Config

class Controller():

    Host_Name = ""
    User_Name = ""
    Password = ""
    Database_Name = ""

    def __init__(self):
        self.conexion = DBConnect()
        self.config = Config()

    def initConection(self):
        return self.config.readConfig()

    def showDatabases(self):
        data = self.conexion.return_data("SHOW SCHEMAS","")
        return data

c = Controller()
print(c.initConection())