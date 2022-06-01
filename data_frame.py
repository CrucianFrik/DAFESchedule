from datetime import datetime
from parsers import ParserDataFrame, ParserGoogleSheet


class DataFrame:
    def __init__(self, resouce, tables=[]):
        print("CREATING DATAFRAME")
        self.__tables = tables
        self.__parser_global = ParserGoogleSheet(resouce, "dataframe_file.xlsx")
        self.__parser_local = None

        self.__update()

        self.__last_update = datetime.now()
        print("DATAFRAME CREATED")

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
        if (msg.need_update()):
            print("TABLES WILL BE UPDATE")
            self.__update()
        df = self.__parser_local.parse(msg)
        return self.__to_json(df)

    def print_tables(self):  # to del
        for i in self.__tables:
            print(i.get___data())

    def __to_json(self, df):
        ans = {"lessons_list": []} #}
        if df.get("error", False):
            return df
        for num, line in df.iterrows():
            try:
                weekday = self.get_table("weekdays").get_data().loc[line[0]].weekday
            except Exception as e:
                weekday = str(e)
            time = self.get_table("times").get_data().loc[line[1]].time
            group = self.get_table("groups").get_data().loc[line[2]].group
            chair = self.get_table("groups").get_data().loc[line[2]].profile

            class_ = '-'
            if str(line[3]).isdigit():
                class_ = str(self.get_table("classes").get_data().loc[line[3]].number)

            teacher = '-'
            if line[4]:
                try:
                    teacher = self.get_table("teachers").get_data().loc[line[4]]
                    teacher = teacher.surname+" "+teacher["name"][0]+"."+teacher.lastname[0]+"."
                except:
                    pass

            subject = '-'
            try:
                subject = line[5]
            except:
                pass

            ans["lessons_list"].append({"group": group, "chair": chair, "day": weekday,"time": time,"subj": subject,"teacher":teacher,"aud":class_})

        return ans

    def __update(self):
        self.__tables = self.__parser_global.parse()
        self.__parser_local = ParserDataFrame(self.__tables)

    def __check_update(self):
        update_time = 20 * 60 * 60
        if (datetime.now() - self.__last_update).seconds > update_time:
            self.__update()
            self.__last_update = datetime.now()
        return True