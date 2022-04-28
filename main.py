from data_frame import DataFrame
from message import Message
tf = DataFrame("1s_u2pPZ3xdu_tBrVy7hriV2xj15OP9evJfVAuzFyZSc")

print()
m = Message()
m.add_request({"teachers": [("surname", "Юдин"),  ("name", "Михаил")]})
print(m.get_content())
print(tf.request(m))
print("-------------------------------------\n")

m = Message()
m.add_request({"teachers": [("surname", "Стремоусов")]})
print(m.get_content())
print(tf.request(m))
print("-------------------------------------\n")

m = Message()
m.add_request({"groups": ("group", "Б03-115")})
m.add_request({"weekdays": ("weekday", "Четверг")})
print(m.get_content())
print(tf.request(m))
print("-------------------------------------\n")

m = Message()
m.add_request({"teachers": [("surname", "Свечников")]})
print(m.get_content())
print(tf.request(m))
print("-------------------------------------\n")
