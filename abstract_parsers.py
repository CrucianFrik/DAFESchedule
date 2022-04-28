class Parser:
    def __init__(self, res):
        self._resource = res


class ParserGlobal(Parser):
    def __init__(self, res):
        super().__init__(res)

    def parse(self):
        pass


class ParserLocal(Parser):
    def __init__(self, res):
        super().__init__(res)

    def parse(self, msg):
        pass
