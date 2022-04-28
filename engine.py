from data_frame import DataFrame


class Engine:
    def __init__(self):
        self.__scheduleData = DataFrame("1s_u2pPZ3xdu_tBrVy7hriV2xj15OP9evJfVAuzFyZSc")

    def schedule_request(self, msg):
        return self.__scheduleData.request(msg)

    def schedule_db_request(self):
        return self.__scheduleData.get_tables()
