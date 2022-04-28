from datetime import datetime
from parsers import ParserDataFrame, ParserGoogleSheet

class DataFrame:
    def __init__(self, resouce, tables=[]):
        self.__tables = tables
        self.__parser_global = ParserGoogleSheet(resouce, "dataframe_file.xlsx")

        self.__update()

        self.__parser_local = ParserDataFrame(self.__tables)
        self.__last_update = datetime.now()

    def add(self, table):
        for t in self.__tables:
            if table.get_name() == t.get_name():
                raise Exception("a table with this name already exists")
        self.__tables.append(table)

    def get_tables(self):
        return self.__tables

    def get_table(self, name):
        for t in self.__tables:
            if t.get_name() == name:
                return t

    def request(self, msg):
        self.__check_update()
        return self.__parser_local.parse(msg)

    def print_tables(self):  # to del
        for i in self.__tables:
            print(i.get___data())

    def __update(self):
        self.__tables = self.__parser_global.parse()

    def __check_update(self):
        update_time = 2 * 60 * 60
        if (datetime.now() - self.__last_update).seconds > update_time:
            self.__update()
        return True

