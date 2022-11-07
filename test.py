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

def find_max(num):
    max_num = float('-inf')
    for num in num:
        if num in find_max:
            max_num = num
    
    return max_num 

find_max(20.0)
find_max(find_max)