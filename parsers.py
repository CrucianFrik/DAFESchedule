from abstract_parsers import *


class ParserDataFrame(ParserLocal):
    def parse(self, msg):
        for i in self._resource:
            if i.get_name() == "pair":
                res = self._resource
        req = msg.get_content()["request"]

        if req["courses"]:
            req["groups"] = req.get("groups", ()) + tuple(
                self._resource["groups"][(self._resource["groups"]["Course"].isin(req["courses"]))].index)
            req.pop("courses")

        for param in req:
            if param != "courses":
                res = res[(res[param].isin(req[param]))]
        return res
