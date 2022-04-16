import Message
import Engine

class Controller:
    def __init__(self):
        self.__engine = Engine()

    def schedule_request(self, group_id=(), course=(), teacher_id=(), class_id=(), weekday_id=(), pair_numbers=()):
        # typle args are expected
        msg = Message()
        msg.add_request(
            {"groups": group_id, "courses": course, "teachers": teacher_id, "classes": class_id, "weekdays": weekday_id,
             "pair_numbers": pair_numbers})
        return self.__engine.schedule_request(msg)

    def schedule_db_request(self):
        return self.__engine.schedule_db_request()

