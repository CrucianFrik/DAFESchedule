import pandas as pd
import numpy as np
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
        try:
            sheet_values = pd.concat([
                self.__get_teacher_and_post("Список преподавателей институск"),
                self.__get_teacher_and_post("Список преподавателей баз.кафед")])
            teachers = Table("teachers", ['surname', 'name', 'lastname', 'post'])

            for i in range(len(sheet_values)):
                teachers.add_line(
                    sheet_values.iloc[i]["Преподаватель"].split() + [sheet_values.iloc[i]["Должность"].lower()])
                '''try:
                    teachers.add_line(
                        sheet_values.iloc[i]["Преподаватель"].split() + [sheet_values.iloc[i]["Должность"].lower()])
                except Exception as e:
                    print(sheet_values.iloc[i])'''

            teachers.sort_by("surname")
            teachers.reset_index()
            print("ParserTeacherTable: completed")
            return teachers
        except Exception as e:
            print("ParserTeacherTable: WARNING!")
            print(e)

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
            #print(list(map(lambda x: str(x), sheet_values.loc[0])))
            classes = list(filter(lambda x: str(x).isdigit(), list(map(lambda x: str(x), sheet_values.loc[0]))))
            print(classes)
            print("ClassTablePU: completed")
            return Table("classes", ["number"], [classes])
        except Exception as e:
            print("ClassTablePU: WARNING!")
            print(e)


class GroupTablePU(GlobalParserUtility):
    def __init__(self, global_parser):
        super().__init__(global_parser)

    def parse(self):
        try:
            groups = Table("groups", ['course', 'group', 'profile'])
            for num in range(1, 7):
                sheet_values = self._global_parser.get_sheet(str(num) + " курс ")
                group_names = list(map(str, filter(lambda x: x and not str(x).isalpha(), sheet_values.loc[1])))
                groups.add_lines(
                    [[num] * len(group_names), group_names, sheet_values.loc[2][2:]])  # (cource, group_name)
            print("ParserGroupTable: complited")
            return groups
        except Exception as e:
            print("ParserClassTable: WARNING!")
            print(e)


class ScheduleTablePU(GlobalParserUtility):
    def __init__(self, teachers, groups, classes, weekdays, times):
        super().__init__(None)
        self.__weekdays = weekdays.get_data()
        self.__times = times.get_data()
        self.__groups = groups.get_data()
        self.__teachers = teachers.get_data()
        self.__classes = classes.get_data()
        self.__schedule_table = Table("pairs",
                                      ["weekdays", "times", "groups", "classes", "teachers", "subject"],
                                      is_values_int=True)

    @staticmethod
    def get_value(pdSeries_len):
        return list(pdSeries_len)[0]

    @staticmethod
    def clear_of_space_chars(st):
        return ' '.join(filter(lambda x: x, st.split()))

    def split_pair_info(self, pair):
        return list(map(self.clear_of_space_chars, pair.split('/')))

    @staticmethod
    def format_snl(snl):  # формат фио
        snl_ = snl.split()
        s = snl_[0]
        if len(snl) != 3:
            n = snl.split('.')[0][-1]
            l = snl.split('.')[1][-1]
        else:
            n = snl_[1][0]
            l = snl_[2][0]
        return (s, n, l)

    @staticmethod
    def is_pair_free(pair):
        return type(pair) != str

    @staticmethod
    def format_schedule_table(df):
        df.loc[1, "Unnamed: 0"] = "weekday"
        df.loc[1, "Unnamed: 1"] = "time"
        profies = pd.Series(['', ''] + list('/' + df.loc[2][2:]))
        group_numbers = list(df.loc[1])[:2] + list(filter(lambda x: str(x) != str(np.nan), list(df.loc[1])[2:]))
        ren = dict(
            zip(list(df.columns), pd.Series(map(lambda x, y: str(x) + y, group_numbers, profies[:len(group_numbers)]))))
        df = df.rename(columns=ren)[3:]
        return df

    def parse(self):
        try:
            sheet_names = list(map(lambda x: str(x) + " курс ", range(1, 7)))  # + ["Аспирантура"]
            for sn in sheet_names:
                df = pd.read_excel('dataframe_file.xlsx', sheet_name=sn, engine="openpyxl")
                df = self.format_schedule_table(df)
                for w in self.__weekdays.itertuples():
                    for t in self.__times.itertuples():
                        for g in self.__groups[self.__groups.course == int(sn[0])].itertuples():  # int(sn[0]) - номер курса
                            pairInfo = self.get_value(
                                df[(df["weekday"] == w.weekday) & (df["time"] == t.time)][g.group + "/" + g.profile])
                            if not self.is_pair_free(pairInfo):
                                pairInfo = self.split_pair_info(pairInfo)
                                subject = pairInfo[0]
                                if len(pairInfo) < 3:
                                    teacher_id = np.nan
                                    class_id = np.nan
                                else:
                                    if pairInfo[2].isdigit():
                                        try:
                                            class_id = self.__classes[self.__classes.number == pairInfo[2]].index[0]
                                        except:
                                            class_id == 'not defined'
                                            print(pairInfo)
                                    else:
                                        class_id = np.nan
                                    try:
                                        teacher_id = 'not defined'
                                        snl = self.format_snl(pairInfo[1])
                                        parsed_teachers = self.__teachers[self.__teachers.surname == snl[0]]
                                        for tch in parsed_teachers.itertuples():
                                            if tch.name[0] == snl[1] and tch.lastname[0] == snl[2]:
                                                teacher_id = tch.Index
                                                break
                                    except:
                                        pass
                                self.__schedule_table.add_line([w.Index, t.Index, g.Index, class_id, teacher_id, subject])
            print("ScheduleTablePU: completed")
            return self.__schedule_table
        except Exception as e:
            print("ScheduleTablePU: WARNING!")
            print(e)
