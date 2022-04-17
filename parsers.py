from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pprint
import io
from files_objects import XlsxFile
from abstract_parsers import *
from global_parser_utilites import TeacherTablePU, GroupTablePU, ClassTablePU
from data_structures import Table


# is not completed
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


class ParserGoogleSheet(ParserGlobal):
    def __init__(self, google_file_id, files_path="ParserGoogleSheetFile.xlsx"):
        super().__init__(google_file_id)
        self.__tables = []

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
            self.__tables.append(TeacherTablePU(self).parse())
            self.__tables.append(GroupTablePU(self).parse())
            self.__tables.append(ClassTablePU(self).parse())
            self.__tables.append(
                Table("weekdays", ["weekday"], [["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]]))
            self.__tables.append(Table("times", ["time"], [
                ["9:00-10:25", "10:35-12:00", "12:10-13:35", "13:45-15:10", "15:20-16:45", "16:55-18:20",
                 "18:25-19:45"]]))
            print(self.__tables[3].get_data())
            print("ParserGoogleSheet: complited")
            return self.__tables
        except Exception as e:
            print("ParserTeacherTable: WARNING!")
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
