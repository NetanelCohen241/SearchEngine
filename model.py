
class model(object):

    def __init__(self):
        self.data = 5
        open("docs.txt", "w+")

    def dat(self):
        return self.data

    def add(self, value):
        print("old value:{0} ".format(self.data))
        self.data=int(value)
        print("new value:{0} ".format(self.data))

    def toSreing(self):
        return str(self.data)
