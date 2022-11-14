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

import time


kodeMengajar = "MPL-" + str(time.time()).rsplit(".", 1)[1]
print(kodeMengajar)