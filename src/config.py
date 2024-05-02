import json

class Config():
    def __init__(self):
        pass

    def readConfig(self):
        jsondata = open('config.json')
        data = json.load(jsondata)
        return data['conn']
    
    def writeConnection(self,host,user,password,database):
        data_list = [host,user,password,database]
        data_json = {}
        json_data = json.dumps(data_list)
        data_json['conn'] = json.loads(json_data)

        json_data = json.dumps(data_json)
        decoded = json.loads(json_data)

        with open('config.json', 'w') as outfile:
            json.dump(decoded, outfile)