import json


def make_tuple(elem):
    return elem if type(elem) == tuple else tuple(elem) if type(elem) == list else tuple([elem])


class Message:
    def __init__(self):
        self.__content = {"request": dict(), "log": ""}

    def add_request(self, args): #ожидается словарь
        for elem in args.items():
            self.__content["request"][elem[0]] = elem[1] #table_name: (column, val)

    def add_log(self, log_text):
        self.__content["log"] = log_text

    def get_content(self):
        return self.__content

    def get_json(self):
        return json.dumps(self.__content, ensure_ascii=False)
