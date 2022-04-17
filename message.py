import json


def make_tuple(elem):
    return elem if type(elem) == tuple else tuple(elem) if type(elem) == list else tuple([elem])


class Message:
    def __init__(self):
        self.__content = dict()

    def add_request(self, args):
        self.__content["request"] = dict(
            filter(lambda x: x, map(lambda x: (x[0], make_tuple(x[1])) if x[1] else (), args.items())))

    def add_log(self, log_text):
        self.__content["log"] = log_text

    def get_content(self):
        return self.__content

    def get_json(self):
        return json.dumps(self.__content, ensure_ascii=False)
