# name = "John Jacob Jingleheimer Schmidt"
# first, *last = name.split()
# print("First = {first}".format(first=first))
# #First = John
# print("Last = {last}".format(last=last))
# #Last = Jacob Jingleheimer Schmidt

# name = 'Ari Saja Lah'
# first_name = ''
# last_name = ''
# first_name, *last_name = name.split()
# if len(last_name) == 0:
#     last_name = first_name
# elif len(last_name) != 0:
#     last_name = " ".join(last_name)

# print(first_name)
# print(last_name)
# # print(" ".join(last_name))

# import time


# kodeMengajar = "MPL-" + str(time.time()).rsplit(".", 1)[1]
# print(kodeMengajar)
# import requests as req

# url = 'http://127.0.0.1:5000/api/v2/auth/get-all'
# resp = req.get(url)
# jsonResp = resp.json()
# data = []
# for i in jsonResp:
#     data.append({'id': i['id']})

# print(jsonResp)

# nama = 'Aura Suci Ambarala'
# get_one = nama.split(sep=' ', maxsplit=1)[1]
# print(get_one)

# data = {'username': 1}

# print(data.get('username'))

# data['nama'] = 'saya'

# print(data)

import json
import os

# data = {"a": 1, "b": 2}

# # data = {"c": 3}
# with open("data.json", "a") as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

# # with open("data.json", "r") as f:
# #     data = json.loads(f.read())
# #     print(data.get('a'))

# with open('data.json') as f:
#     data = json.load(f)
#     y = {'c': 3}
#     data['c'] = y['c']

#     json.dump(data, f)


# def write_json(data, filename="data.json"):
#     with open(filename, "w") as f:
#         json.dump(data, f, indent=4)


# with open("data.json") as json_file:
#     data = json.load(json_file)
#     temp = data
#     print(temp)
#     y = {"c": 3}
#     temp["c"] = y["c"]


# def write_json(data, filename="data.json"):
#     file = open(filename, "w+")
#     to_json = json.dump(obj=data, fp=file)
#     file.write()
#     return to_json


# # # def delete_json(data, filename='data.json'):
# # #     file = open(filename, 'w')
# # #     delete = j

# # filename = open("data.json")
# # data = json.load(filename)
# # temp = data
# # y = {"c": 3}
# # temp["c"] = y["c"]
# data = {"a": 1}
# write_json(data)

# # with open("data.json") as json_file:
# #     data = json.load(json_file)
# #     temp = data
# #     print(temp)
# #     y = {"d": 4}
# #     temp["d"] = y["d"]
# with open("data.json") as file_json:
#     data = json.load(file_json)
#     data.clear()
# write_json(data)

# json_file = os.getcwd() + "/data.json"
# with open(json_file) as file_json:
#     data = json.load(dict(file_json))

# print(data)
# root = os.path.realpath(os.path.dirname(__file__))
# print(os.path.join(root, "data.json"))
# data = os.path.join(root, "data.json")
# f = open(data)
# print(f.read())

# n = 1
# while n <= 5:
#     print(n)
#     n += 1

# for n in range(1, 5 + 1):
#     siswa = f"sisa{n}"
#     sisa = f"u{n}"
#     print(siswa)
#     print(sisa)

# from app.backend.lib.date_time import today_
# import time
# import calendar
import datetime

# # print(today_())

# # time = time.localtime()

# # print(time.tm_wday)

# # call = calendar
# # print(call.calendar(2022, 3))

# dt = datetime.datetime.date(datetime.datetime.today())
# week = datetime.datetime.today().weekday()
# print(dt)
# print(week)

# from math import ceil


# def week_of_month(dt):
#     """Returns the week of the month for the specified date."""

#     first_day = dt.replace(day=1)

#     dom = dt.day
#     adjusted_dom = dom + first_day.weekday()

#     return int(ceil(adjusted_dom / 7.0))


# print(week_of_month(datetime.datetime.date(datetime.datetime.today())))
# for i in range(1, 5 + 1):
#     # print(i * "*")
#     # print((2 * i - 1) * "*")
#     # print((2 * i) * "*")
#     # print((5 - i + 1) * "*")
#     # print((5 - i) * " " + (2 * i - 1) * "*")
#     print((5 - i + 1) * "*")
import calendar
from datetime import datetime

for i in range(1, 13):
    bulan = calendar.month_name[i]
    print(bulan)
# dt = datetime.datetime.date(datetime.datetime.today())
dt = datetime.date(datetime.today())
print(dt)
