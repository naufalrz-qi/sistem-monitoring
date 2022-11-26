import json


class JsonFileObject:
    def __init__(self, filename) -> None:
        self.filename = filename

    def write_json(self, data):
        f = open(self.filename, "w+")
        toJsonFile = json.dump(data, f)
        return toJsonFile

    def get_json(self):
        f = open(self.filename)
        fromObject = json.load(f)
        return fromObject

    def clear_json(self):
        data = self.get_json()
        data.clear()
        return self.write_json(data)

    def cetak_data(self):
        data = self.get_json()
        print(f"data from file : {data}")
