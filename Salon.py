class Salon():
    def __init__(self, id, location, name):
        self.id = id
        self.location = location
        self.name = name
    id = 0
    location = 0
    name = "no name"
    def CreateSalon(self):
        f = open("Salon.txt", "a+")
        lines = f.readlines()
        for l in lines:
            if l != str(self.id) + ";" + str(self.location) + ";" + str(self.name)+"\n":
                f.write(str(self.id) + ";" + str(self.location) + ";" + str(self.name)+"\n")
            else:
                pass
        f.close()
    def getAllSalons(self):
        f = open("Salon.txt", "r")
        lines = f.readlines()
        for l in lines:
            print(l.strip())
        f.close()
    def getAllSorted(self):
        pass
    def getSalonById(self, list, id):
        pass
    def deleteSalon(self):
        pass

