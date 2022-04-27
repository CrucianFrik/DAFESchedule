import pandas as pd
from table import Table


def expand_line(n, symbol):
    symbol = " " + symbol
    return lambda s: str(s) + symbol * (n - len(str(s).split())) if s else symbol * n


class GlobalParserUtility:
    def __init__(self, global_parser):
        self._global_parser = global_parser

    def parse(self):
        pass


class TeacherTablePU(GlobalParserUtility):
    def __init__(self, global_parser):
        super().__init__(global_parser)

    def parse(self):
        #try:
        sheet_values = pd.concat([
            self.__get_teacher_and_post("Список преподавателей институск"),
            self.__get_teacher_and_post("Список преподавателей баз.кафед")])
        teachers = Table("teachers", ['surname', 'name', 'lastname', 'post'])

        for i in range(len(sheet_values)):
            try:
                teachers.add_line(
                    sheet_values.iloc[i]["Преподаватель"].split() + [sheet_values.iloc[i]["Должность"].lower()])
            except Exception as e:
                print(sheet_values.iloc[i])

        teachers.sort_by("surname")
        teachers.reset_index()
        print("ParserTeacherTable: completed")
        return teachers
        #except Exception as e:
         #   print("ParserTeacherTable: WARNING!")
          #  print(e)

    def __get_teacher_and_post(self, sheet_name):
        df = self._global_parser.get_sheet(sheet_name)
        df["Преподаватель"] = df["Преподаватель"].apply(expand_line(3, "-"))
        df["Должность"] = df["Должность"].apply(expand_line(1, "-"))
        teachers = df[["Преподаватель", "Должность"]]
        return teachers


class ClassTablePU(GlobalParserUtility):
    def __init__(self, global_parser):
        super().__init__(global_parser)

    def parse(self):
        try:
            sheet_values = self._global_parser.get_sheet("аудиторный фонд")
            classes = list(filter(lambda x: str(x).isdigit(), sheet_values.loc[0]))
            print("ParserClassTable: completed")
            return Table("classes", ["number"], [classes])
        except Exception as e:
            print("ParserClassTable: WARNING!")
            print(e)


class GroupTablePU(GlobalParserUtility):
    def __init__(self, global_parser):
        super().__init__(global_parser)

    def parse(self):
        try:
            groups = Table("groups", ['course', 'group', 'profile'])
            for num in range(1, 7):
                sheet_values = self._global_parser.get_sheet(str(num) + " курс ")
                group_names = list(filter(lambda x: x and not str(x).isalpha(), sheet_values.loc[1]))
                groups.add_lines(
                    [[num] * len(group_names), group_names, sheet_values.loc[2][2:]])  # (course, group_name)
            print("ParserGroupTable: completed")
            return groups
        except Exception as e:
            print("ParserClassTable: WARNING!")
            print(e)
