from data_structures import DataFrame


class Engine:
    def __init__(self):
        self.__scheduleData = DataFrame()

    def schedule_request(self, msg):
        return self.__scheduleData.request(msg)

    def schedule_db_request(self):
        return self.__scheduleData.get_tables()
