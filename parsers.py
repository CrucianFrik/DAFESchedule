import pandas as pd
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pprint
import io
from files_objects import XlsxFile
from abstract_parsers import *
from global_parser_utilites import TeacherTablePU, GroupTablePU, ClassTablePU, ScheduleTablePU
from table import Table


class ParserDataFrame(ParserLocal):
    def __init__(self, res):
        super().__init__(res)

    def get_table_data(self, name):
        for i in self._resource:
            if i.get_name() == name:
                return i.get_data()

    def parse(self, msg):
        sch_tab = self.get_table_data("pairs")
        for tb_name, req in msg.get_content()["request"].items():
            if type(req) != list:
                req = [req]

            for r in req:
                try:
                    ans = pd.DataFrame()
                    clm, val = r
                    t = self.get_table_data(tb_name)
                    ids = t[t[clm] == val].index
                    for id in ids:
                        ans = pd.concat([ans, sch_tab[sch_tab[tb_name] == id]])
                    sch_tab = ans
                except Exception as e:
                    print("WARNING IN LOCAL PARSER:")
                    print(e)
                    return pd.DataFrame({"-": [req]})
        return ans


class ParserGoogleSheet(ParserGlobal):
    def __init__(self, google_file_id, files_path="dataframe_file.xlsx"):
        super().__init__(google_file_id)
        self.__init_service_acc()

        self.__xlsx = self.__download_xlsx(google_file_id, files_path)
        self.__xlsx.unmerge_cells()

    def get_sheet(self, name):
        return self.__xlsx.get_sheet(name)

    def save(self, name):
        self.__xlsx.save(name)

    def __getitem__(self, item):
        for t in self.__tables:
            if t.get_name() == item:
                return t

    def parse(self):
        try:
            print("ParserGoogleSheet: parsing started")
            tables = []
            tables.append(TeacherTablePU(self).parse())
            tables.append(GroupTablePU(self).parse())
            tables.append(ClassTablePU(self).parse())
            tables.append(
                Table("weekdays", ["weekday"], [["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]]))
            tables.append(Table("times", ["time"], [
                ["9:00-10:25", "10:35-12:00", "12:10-13:35", "13:45-15:10", "15:20-16:45", "16:55-18:20",
                 "18:25-19:45"]]))
            tables.append(ScheduleTablePU(*tables).parse())
            print("ParserGoogleSheet: complited")
            return tables
        except Exception as e:
            print("ParserGoogleSheet: WARNING!")
            print(e)

    def __init_service_acc(self):
        _scopes = ['https://www.googleapis.com/auth/drive']
        _service_account_file = 'central-diode-342919-c35aafd1b173.json'
        credentials = service_account.Credentials.from_service_account_file(
            _service_account_file, scopes=_scopes)
        pp = pprint.PrettyPrinter(indent=4)
        self.__service = build('drive', 'v3', credentials=credentials)

    def __download_xlsx(self, google_file_id, path):
        file_id = google_file_id
        request = self.__service.files(). \
            export_media(fileId=file_id,
                         mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        filename = path
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download .xlsx file %d%%." % int(status.progress() * 100))
        return XlsxFile(path)
