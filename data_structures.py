class DataFrame:
    def __init__(self, resouce, tables=[]):
        self.__tables = tables
        self.__parse_global = ParserGoogleSheet(resouce, "__dataframe_file.xlsx")

        self.__update()

        self.__parser_local = Parser__dataFrame(self.__tables)
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


class Table:
    def __init__(self, name, columns, lines=[], is_values_int=False):
        self.__name = name
        self.__columns = columns
        if not lines:
            lines = [pd.Series()] * len(columns)
        self.__data = pd.DataFrame(self.__make_dir(columns, lines))
        if is_values_int:
            self.__data = self.__data.convert_dtypes()

    def add_line(self, line):
        self.__data = self.__data.append(self.__make_dir(self.__data.columns, line), ignore_index=True)

    def add_lines(self, columns):
        for line in zip(*columns):
            self.add_line(line)

    def get_data(self):
        return self.__data

    def get_name(self):
        return self.__name

    def sort_by(self, param):
        self.__data = self.__data.sort_values(by=param)

    def reset_index(self):
        self.__data = self.__data.reset_index()
        del self.__data["index"]

    def __make_dir(self, keys, values):
        return {k: v for k, v in zip(keys, values)}

    def __getitem__(self, item):
        for c in self.__colomns:
            if item in list(self.__data[c]):
                return self.__data[self.__data[c] == item]
