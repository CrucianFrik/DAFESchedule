import json


def make_tuple(elem):
    return elem if type(elem) == tuple else tuple(elem) if type(elem) == list else tuple([elem])

class RequestError(Exception):
    def __init__(self, message="Ошибка запроса к парсеру"):
        self.message = message
        super().__init__(self.message)


class Message:
    def __init__(self, json_=None):
        self.__content = {'request': dict(), 'update': False}
        if json_:
            self.__load(json_)
        print("MESSAGE::__content: ", self.__content)
        try:
            self.__check_content()
        except Exception as e:
            print("ERROR in class Message: ", e)
            raise e

    def add_request(self, args): #ожидается словарь
        for elem in args.items():
            self.__content['request'][elem[0]] = elem[1] #table_name: (column, val)

    def get_content(self):
        return self.__content

    def get_json(self):
        return json.dumps(self.__content, ensure_ascii=False)

    def add_update(self):
        self.__content['update'] = True

    def need_update(self):
        return self.__content['update']

    def __load(self, json_):
        for req_elem in ["teachers", "groups"]:
            if json_.get(req_elem, False) != False:
                if json_[req_elem]:
                    self.__content['request'][req_elem] = []
                    for elem in json_[req_elem]:
                        line = {}
                        for gap, val in elem.items():
                            if val:
                                line[gap] = self.__check_makros(gap, val)
                        if line:
                            self.__content['request'][req_elem].append(line)
                json_.pop(req_elem)

        for req_elem, column in zip(["classes", "weekdays", "times"], ["number", "weekday", "time"]):
            if json_.get(req_elem, False) != False:
                if json_[req_elem]:
                    self.__content['request'][req_elem] = list(map(lambda val: {column: self.__check_makros(req_elem, val)}, json_[req_elem]))
                json_.pop(req_elem)

        if len(json_) != 0:
            raise RequestError("В запросе присутствуют лишние поля (проверьте: возможно, вы допустили опечатку)")

    def __check_content(self):
        if not self.__content.get("request"):
            raise RequestError("В запросе отсутствует поле 'request'")

        if self.__content.get("update") == None:
            self.__content["update"] = False

        if len(self.__content) > 2:
            raise RequestError("Некорректное количество полей в запросе. Необходимые: 'request'; опциональные: 'update'")

    def __check_makros(self, gap, val):
        if gap == "surname":
            if val.lower() == "хых":
                return "Сизых"

            if val.lower() == "серыч":
                return "Серохвостов"

            if val.lower() == "бур":
                return "Бурмистров"

            if val.lower() == "беспорт":
                return "Беспорточный"

            if val.lower() == "жиж":
                return "Животов"

            if val.lower() in ["гречников", "удод мохнатый"]:
                return "Свечников"

            if val.lower() == "сказочник":
                return "Фёдоров"

        if gap == "group":
            if val.isdigit() and val[0] != "8":
                return "Б03-"+val

        if gap == "classes":
            if val.lower() == "бма":
                return "306"

            if val.lower() == "бфа":
                return "314"

        return val

