import pandas as pd


class Table:
    def __init__(self, name, columns, lines=[], is_values_int=False):
        self.__name = name
        self.__columns = columns
        if lines:
            self.__data = pd.DataFrame(self.__make_dir(columns, lines))
        else:
            self.__data = pd.DataFrame({c: pd.Series(dtype=t) for c, t in zip(columns, ['str']*len(columns))})
        if is_values_int:
            self.__data = self.__data.convert_dtypes()

    def add_line(self, line):
        li = [self.__data, pd.DataFrame.from_dict(self.__make_dir(self.__data.columns, map(lambda x: [x], line)))]
        self.__data = pd.concat(li, ignore_index=True)

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
        for c in self.__columns:
            if item in list(self.__data[c]):
                return self.__data[self.__data[c] == item]
