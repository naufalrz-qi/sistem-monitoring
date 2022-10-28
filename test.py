# name = "John Jacob Jingleheimer Schmidt"
# first, *last = name.split()
# print("First = {first}".format(first=first))
# #First = John
# print("Last = {last}".format(last=last))
# #Last = Jacob Jingleheimer Schmidt

name = 'Ari Efendi Saja'
first_name, *last_name = name.split()

print(first_name)
print(" ".join(last_name))