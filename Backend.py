import Json_data
import datetime
import json
import random
import os

date_today = datetime.datetime.today()


class General:
    """initiate initial values"""

    def __init__(self):
        self.date = None
        self.number = None

    @staticmethod
    def getId():
        """get a random no for unique id"""
        string = str(date_today.isoformat()) + str(random.randint(0, 9999))

        return ''.join(char for char in string if char.isalnum())

    def convertDateFormat(self, date):
        """its return data format in required format"""
        self.date = date

        data = self.date[0:10]
        val = data.split('-')
        date_string = str(val[2]) + '-' + val[1] + '-' + val[0]
        return date_string

    def convertTimeFormat(self, date):
        """its get date and time in the required format"""
        self.date = date

        time = self.date[11:]
        date = self.date[5:10]
        dates = date.split('-')
        val = time.split(':')

        def getAmORPm(num):
            """return am or pm"""
            if num >= 12:
                return 'PM'
            else:
                return 'AM'

        time_string = dates[1] + '/' + dates[0] + "  " + str(int(val[0]) % 12) + ':' + val[1] + ' ' + getAmORPm(
            int(val[0]))
        return time_string

    def convert_to_currency(self, number):
        """ converty a string to a currency format"""
        self.number = number
        s, *d = str(self.number).partition(".")
        r = ",".join([s[x - 2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d)

    @staticmethod
    def getNoOfTables():
        """return no on tables from json file"""
        path_dir = os.path.join('General.json')
        try:
            jsonFile = open(path_dir, "r")
            list_data = json.load(jsonFile)
            if list_data['No of Tables'] > 30:
                return 30
            else:
                return list_data['No of Tables']
        except BaseException:
            return 30

    def log_entry(self, place=0, where='', message=""):
        """this is for tracking of any error logs to display"""
        self.place = place
        self.where = where
        self.message = message

        check_log = os.path.isfile('Senior.txt')

        if not check_log:
            with open('logs.txt', 'w') as fp:
                pass

        with open('logs.txt', 'a') as fp:
            fp.write(str(datetime.datetime.now()) + "\t" + str(self.place) + "\t" +
                     str(self.where) + "\t" + str(self.message) + "\n")
            fp.close()


class Billing:
    def __init__(self):
        self.table_no = None
        self.object_id = None
        self.bill_tree = None
        self.main = None
        self.sub = None

    @staticmethod
    def getItemsList():
        """Its get the items from the stock data"""
        main_types = []

        with open(Json_data.JsonFile().getJsonPath('Stock'), 'r') as file:
            lst = json.load(file)

        for i in lst:
            main_types.append(i['main'].lower() + " - " + i['sub'].lower())

        return main_types

    @staticmethod
    def getActiveTables():
        """get the no of tables are active"""
        tables = set()
        with open(Json_data.JsonFile().getJsonPath('Active'), 'r') as file:
            lst = json.load(file)

        for i in lst:
            tables.add(i['table no'])

        return tables

    def getObjectId(self, main, sub):
        """its return the id by passing the maintype and subtype"""
        self.main = main
        self.sub = sub

        with open(Json_data.JsonFile().getJsonPath('Stock'), 'r') as file:
            lst = json.load(file)

        try:
            for i in lst:
                if i['main'] == self.main and i['sub'] == self.sub:
                    return i
        except BaseException as msg:
            General.log_entry(125, 'getObjectId', msg)

    def checkIfExisted(self, bill_tree, object_id):
        """its check the id are already existed in the tree"""

        self.bill_tree = bill_tree
        self.object_id = object_id

        if self.object_id == "":
            return None

        else:
            for line in self.bill_tree.get_children():
                items = self.bill_tree.item(line)['values']
                if self.object_id == items[0]:
                    return line

    def checkTreeSelected(self, bill_tree=None):
        """check a tree if existed or not"""
        self.bill_tree = bill_tree

        items = self.bill_tree.selection()
        records = self.bill_tree.item(items, "values")
        for i in records:
            if i is not None:
                return True
            else:
                return False

    def convertTreeToList(self, bill_tree=None):
        """its converts the tree object to the list data"""
        self.bill_tree = bill_tree
        list_tree = []
        try:
            for line in self.bill_tree.get_children():
                items = self.bill_tree.item(line)['values']
                if items[0] == '':
                    items[0] = '0'
                list_tree.append(items)

        except BaseException as msg:
            General.log_entry(125, 'getObjectId', msg)
        return list_tree

    def getTotalAmount(self, bill_tree=None):
        """by passing tree we get the total amount of the tree"""
        self.bill_tree = bill_tree
        amount = 0
        for line in self.bill_tree.get_children():
            items = self.bill_tree.item(line)['values']
            amount += items[4]
        return amount

    def checkTreeExisted(self, bill_tree):
        """its check if data is existed or not in the tree"""
        self.bill_tree = bill_tree
        for line in self.bill_tree.get_children():
            items = self.bill_tree.item(line)['values']
            if items is not None:
                return True
            else:
                return False

    def submitData(self, table_no=0):
        """convert the active data to bills json"""
        self.table_no = table_no

        data = Active().getTableData(self.table_no)
        for i in data:
            i['sl_no'] = Bills().getSlNo()
            i['final_time'] = date_today.isoformat()
            Json_data.JsonFile().addDataToJson('Bills', i)


class Stock:
    def __init__(self):
        self.items = None
        self.search = None
        self._object_id = None
        self._main_item = None
        self._sub_item = None
        self._rate = None

    def addNew(self, main_item, sub_item, rate):
        """adds data to the stock json"""
        self._main_item = main_item
        self._sub_item = sub_item
        self._rate = rate

        s_data = {'_id': General.getId(), 'main': self._main_item.title(),
                  "sub": self._sub_item.title(), 'rate': self._rate,
                  'date': date_today.isoformat()}

        Json_data.JsonFile().addDataToJson('Stock', s_data)
        return True

    def updateStock(self, object_id, main_item, sub_item, rate):
        """update stock"""
        self._object_id = object_id
        self._main_item = main_item
        self._sub_item = sub_item
        self._rate = rate

        u_data = {'_id': self._object_id, 'main': self._main_item.title(),
                  'sub': self._sub_item.title(), 'rate': self._rate,
                  'date': date_today.isoformat()}

        Json_data.JsonFile().updateJsonData("Stock", self._object_id, u_data)
        return True

    @staticmethod
    def getAllStock():
        """get all the stock from the json data"""
        return Json_data.JsonFile().readJsonData('Stock')

    def getSearchStock(self, search):
        """its search the data from the json data """
        self.search = search
        list_data = []

        with open(Json_data.JsonFile().getJsonPath('Stock'), 'r') as file:
            lst = json.load(file)

        for i in lst:
            if i['main'] == self.search or i['sub'] == self.search:
                list_data.append(i)

        return list_data

    def getTypesData(self, items):
        """by passing the data its gets the type of elements"""
        self.items = items
        list_data = set()

        lst = self.getAllStock()

        for i in lst:
            if self.items.lower() == 'main':
                list_data.add(i['main'].lower())

            elif self.items.lower() == 'sub':
                list_data.add(i['sub'].lower())

            else:
                list_data.add(i['main'].lower())
                list_data.add(i['sub'].lower())

        return list_data

    def checkIfAlreadyExist(self, main_item, sub_item):
        """its verifies the stock if already existed in database"""
        self._main_item = main_item
        self._sub_item = sub_item

        lst = self.getAllStock()
        existed = False

        for i in lst:
            if i['main'].title() == self._main_item.title() and \
                    i['sub'].title() == self._sub_item.title():
                existed = True
                break
        return existed


class Bills:
    def __init__(self):
        self.sl_no = None
        self._object_id = None
        self.tree = None
        self._table_no = None
        self._list_data = None
        self._amount = None
        self._initial_time = None
        self._final_time = None
        self._table_no = None

    def addBilling(self, sl_no, table_no, list_data, amount, initial_time, final_time):
        """add bills to the bills"""
        self.sl_no = sl_no
        self._table_no = table_no
        self._list_data = list_data
        self._amount = amount
        self._initial_time = initial_time
        self._final_time = final_time

        b_data = {'_id': General().getId(), "sl_no": self.getSlNo(), 'table_no': self._table_no,
                  'list_data': self._list_data,
                  'amount': self._amount, 'initial_time': self._initial_time, 'final_time': self._final_time}

        Json_data.JsonFile().addDataToJson('Bills', b_data)

    def getTreeData(self, tree):
        """get the records of the bills as the table no"""
        self.tree = tree

        items = self.tree.selection()
        records = self.tree.item(items, "values")

        return records

    @staticmethod
    def getBillData():
        """return all the bill's data from json data"""
        return Json_data.JsonFile().readJsonData('Bills')

    def getDataById(self, object_id):
        """its gets the data buy the id from bills"""
        self._object_id = object_id

        with open(Json_data.JsonFile().getJsonPath('Bills'), 'r') as file:
            lst = json.load(file)

        for i in lst:
            if i['_id'] == self._object_id:
                return i
        file.close()

    @staticmethod
    def getSlNo():
        """its get the max no from the bills if existed"""
        lst = Json_data.JsonFile().readJsonData('Bills')
        sl_no = []
        for i in lst:
            try:
                sl_no.append(i['sl_no'])
            except BaseException as msg:
                pass

        if sl_no:
            return max(sl_no) + 1
        else:
            return 1

    def getDataByTableNO(self, table_no):
        """get bills data by table no"""
        self._table_no = table_no

        lst = Json_data.JsonFile().readJsonData('Bills')
        data = []

        for i in lst:
            if i['table no'] == self._table_no:
                data.append(i)
        return data


class Active:
    def __init__(self):
        self._object_id = None
        self._table_no = None
        self._list_data = None
        self._amount = None

    def addTable(self, table_no, list_data, amount):
        """add data to the active tables"""
        self._table_no = table_no
        self._list_data = list_data
        self._amount = amount

        a_data = {'_id': General().getId(), 'table no': self._table_no, 'items': self._list_data,
                  'amount': self._amount,
                  'initial time': date_today.isoformat()}

        Json_data.JsonFile().addDataToJson('Active', a_data)

    def updateTable(self, table_no, list_data, amount):
        """update the active table data"""
        self._table_no = table_no
        self._list_data = list_data
        self._amount = amount

        with open(Json_data.JsonFile().getJsonPath('Active'), 'r') as file:
            lst = json.load(file)

        try:
            for i in lst:
                if i['table no'] == self._table_no:
                    i['items'] = self._list_data
                    i['amount'] = self._amount
        except BaseException:
            pass

        with open(Json_data.JsonFile().getJsonPath('Active'), 'w') as file:
            json.dump(lst, file)

    def checkTableExisted(self, table_no):
        """check if 6table is existed or not"""
        self._table_no = table_no

        with open(Json_data.JsonFile().getJsonPath('Active'), 'r') as file:
            lst = json.load(file)

        for i in lst:
            if i['table no'] == self._table_no:
                return i

    def delTable(self, table_no):
        """delete the active table from hear"""
        self._table_no = table_no
        with open(Json_data.JsonFile().getJsonPath('Active'), 'r') as file:
            lst = json.load(file)

        for i in lst:
            if i['table no'] == self._table_no:
                lst.remove(i)

        with open(Json_data.JsonFile().getJsonPath('Active'), 'w') as file:
            json.dump(lst, file)

    def getTableData(self, table_no):
        """get all table data"""
        self._table_no = table_no
        list_data = []

        with open(Json_data.JsonFile().getJsonPath('Active'), 'r') as file:
            lst = json.load(file)

        try:
            for i in lst:
                if i['table no'] == self._table_no:
                    list_data.append(i)
        except BaseException as msg:
            print(msg)

        file.close()
        return list_data
