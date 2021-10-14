import ujson as json
# import concurrent.futures


filename = 'data.txt'
def writeJson(data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def readJson():
    with open(filename) as json_file:
        return json.load(json_file)

def readJson(filename):
    with open(filename) as json_file:
        return json.load(json_file)

def writeJson(data,Filename):
    with open(Filename, 'w') as outfile:
        json.dump(data, outfile)

# _pool = concurrent.futures.ThreadPoolExecutor()

# class DataModel():
#     def __init__(self):
#         print("init")
#         self._data = _pool.submit(readJson, 1)

#     def retrieve_data(self):
#         print("retrieving data")
#         return self._data.result()


# class WriterTask(threading.Thread):
#    def __init__(self, data, filename):
#       threading.Thread.__init__(self)
#       self.data = data
#       self.filename = filename
#    def run(self):
#       writeJson(self.data,self.filename)
#       print("Finished writing to a file in background")

# if __name__ == "__main__":
#     data = readJson("liberty.txt")
