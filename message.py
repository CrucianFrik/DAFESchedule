import json


def make_tuple(elem):
    return elem if type(elem) == tuple else tuple(elem) if type(elem) == list else tuple([elem])

class RequestError(Exception):
    def __init__(self, message="Ошибка запроса к парсеру"):
        self.message = message
        super().__init__(self.message)


class Message:
    def __init__(self, json_=None):
        self.__content = {'request': dict(), 'log': "", 'update': False}
        if json_:
            self.__content = json_
        try:
            self.__check_content()
        except Exception as e:
            print("ERROR in class Message: ", e)
            raise e

    def add_request(self, args): #ожидается словарь
        for elem in args.items():
            self.__content['request'][elem[0]] = elem[1] #table_name: (column, val)

    def add_log(self, log_text):
        self.__content['log'] = log_text

    def get_content(self):
        return self.__content

    def get_json(self):
        return json.dumps(self.__content, ensure_ascii=False)

    def check(self, flag):
        return flag

    def add_update(self):
        self.__content['update'] = True

    def need_update(self):
        return self.__content['update']

    def __check_content(self):
        if not self.__content.get("request"):
            raise RequestError("В запросе отсутствует поле 'request'")

        if self.__content.get("log") == None:
            raise RequestError("В запросе отсутствует поле 'log'")

        if self.__content.get("update") == None:
            raise RequestError("В запросе отсутствует поле 'update'")

        if len(self.__content) != 3:
            raise RequestError("Некорректное количество полей в запросе. Необходимые: 'request', 'log', 'update'")