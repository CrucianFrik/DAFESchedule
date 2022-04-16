class Parser:
    def __init__(self, res):
        self._resource = res

    def parse(self):
        pass


class ParserGlobal(Parser):
    def __init__(self, res):
        super().__init__(res)


class ParserLocal(Parser):
    def __init__(self, res):
        super().__init__(res)
