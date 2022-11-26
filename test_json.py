# import json


# def write_json(data):
#     f = open("data.json", "w+")
#     toJson = json.dump(data, f)
#     return toJson


# data = {"a": 1}
# write_json(data)

# # with open("data.json", "r+") as f:
# #     data = json.load(f)
# #     data.clear()
# # print(data)
# # write_json(data)


# def get_json():
#     f = open("data.json")
#     fromJson = json.load(f)
#     return fromJson


# def clear_json():
#     data = get_json()
#     # print(data)
#     data.clear()
#     return write_json(data)


# print(clear_json())


import json


class JsonFilebject:
    def __init__(self, filename=None) -> None:
        self.filename = filename

    def write_json(self, data):
        f = open(self.filename, "w+")
        toJsonFile = json.dump(data, f)
        return toJsonFile

    # get json menggunakan method normal
    def get_jsons(self):
        f = open(self.filename)
        fromObject = json.load(f)
        return fromObject

    # menggunakan method normal
    def clear_json(self):
        data = self.get_jsons()
        data.clear()
        return self.write_json(data)

    # Get json Menggunakan Static Method
    @staticmethod
    def get_json(filename):
        # f = open(self.filename)
        f = open(filename)
        fromObject = json.load(f)
        return fromObject

    # Menggunakan classmethod (tidak dapat memanggil method normal)
    # mengambil data dari staticmethod
    @classmethod
    def cetak_json(cls, filename):
        data = cls.get_json(filename)
        print(data)


def main():
    t = JsonFilebject("data.json")

    data = t.get_jsons()
    # data["a"] = 1
    # data["b"] = 2
    data = {"c": 3, "d": 4}

    t.write_json(data)

    # t.cetak_json(filename="data.json")


if __name__ == "__main__":
    main()
