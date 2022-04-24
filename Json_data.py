import json
import os

os.chdir(os.path.expanduser('~/Documents'))


class JsonFile:
    def __init__(self):
        """Initial values to assign"""

        self.data_list = None
        self.object_id = None
        self.data = None
        self.collection = None
        # this assign path directory and add a hotel folder to path
        self.path_dir = os.path.join('Hotel')

        # this check the directory exists or not
        # if existed nothing happens
        if os.path.isdir(self.path_dir):
            pass
        # if not existed seems its creates a directory and add a empty list to it fou further
        # implementation
        else:
            os.makedirs(self.path_dir)
            lst = []
            initial_data = {"No of Tables": 30, "Pdf path": "D:\\new", "Printer": "Default"}
            with open('General.json', 'w') as fp:
                json.dump(initial_data, fp)
            with open(os.path.join(self.path_dir, 'Bills.json'), 'w') as fp:
                json.dump(lst, fp)
            with open(os.path.join(self.path_dir, 'Stock.json'), 'w') as fp:
                json.dump(lst, fp)
            with open(os.path.join(self.path_dir, 'Active.json'), 'w') as fp:
                json.dump(lst, fp)

    def getJsonPath(self, collection):
        """this get the json path for the pass json file as collection"""
        self.collection = collection

        file_path = os.path.join(self.path_dir, f'{self.collection}.json')
        # if existed its return the path file
        if os.path.isfile(file_path):
            return file_path
        # if not existed seems its create a new json file with that name
        else:
            lst = []
            with open(os.path.join(self.path_dir, f'{self.collection}.json'), 'w') as fp:
                json.dump(lst, fp)

    def addDataToJson(self, collection, data):
        """by passing collection name and data as list this add the Directory  to the collection
        json file"""
        self.collection = collection
        self.data = data
        with open(self.getJsonPath(self.collection), 'r') as file:
            lst = json.load(file)

        lst.append(self.data)

        with open(self.getJsonPath(self.collection), 'w') as file:
            json.dump(lst, file)

    def readJsonData(self, collection):
        """This return the whole data existed in the collection json File"""
        self.collection = collection

        with open(self.getJsonPath(self.collection), 'r') as file:
            lst = json.load(file)
        return lst

    def deleteJsonData(self, collection, object_id):
        """By passing matching ID and the collection name its delete the Directory"""
        self.collection = collection
        self.object_id = object_id

        with open(self.getJsonPath(self.collection), 'r') as file:
            lst = json.load(file)
        try:
            for i in lst:
                if i['_id'] == self.object_id:
                    lst.remove(i)
        except BaseException:
            pass

        with open(self.getJsonPath(self.collection), 'w') as file:
            json.dump(lst, file)

    def updateJsonData(self, collection, object_id, data_list):
        """ by passing the collection name and id and list it updates the data passed """
        self.collection = collection
        self.object_id = object_id
        self.data_list = data_list

        with open(self.getJsonPath(self.collection), 'r') as file:
            lst = json.load(file)
        try:
            for i in lst:
                if i['_id'] == self.object_id:
                    i = self.data_list
                    break
        except BaseException:
            pass
        with open(self.getJsonPath(self.collection), 'w') as file:
            json.dump(lst, file)
