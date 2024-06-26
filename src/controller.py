from src.dbConnect import DBConnect
from src.config import Config

class Controller():

    Host_Name = ""
    User_Name = ""
    Password = ""
    Database_Name = ""

    isConnected = False

    def __init__(self):
        pass

    def initConection(self):
        r = self.config.readConfig()
        connOk = self.conexion.connectiondb(r[0],r[1],r[2],r[3])
        if connOk == True:
            self.isConnected = True
            return True
        else:
            return connOk
        

    def showDatabases(self):
        data = self.conexion.return_data("SHOW SCHEMAS","")
        return data
