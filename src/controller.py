from src.dbConnect import DBConnect
from src.config import Config

class Controller():

    Host_Name = ""
    User_Name = ""
    Password = ""
    Database_Name = ""

    isConnected = False

    def __init__(self):
        print("inicia DBConnect")
        self.conexion = DBConnect()
        print("termina DBConnect")
        print("inicia Config")
        self.config = Config()
        print("termina config")
        pass

    def initConection(self):
        print("inicia initConection")
        print("inicia readConfig")
        r = self.config.readConfig()
        print("termina readConfig")
        connOk = self.conexion.connectiondb(r[0],r[1],r[2],r[3])
        if connOk == True:
            self.isConnected = True
            print("termina initConection con true")
        else:
            print("termina initConection con false")
            return connOk
        

    def showDatabases(self):
        data = self.conexion.return_data("SHOW SCHEMAS","")
        return data
