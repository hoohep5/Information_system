class Salon():
    def __init__(self, id = '00', location = 'none', name= "none"):
        self.id = id
        self.location = location
        self.name = name
    id = 0
    location = 0
    name = "no name"

    def checkCopy(self, p):
        flag = False
        f = open("Salon.txt", "r")
        lines = f.readlines()
        SalonID = []
        for l in lines:
            l = l.replace("\n", "")
            l = l.split(";")
            SalonID.append(l)
        for i in SalonID:
            if (i[0] == p.id or i[1] == p.location or i[2] == p.name):
                flag = True
        return flag

    def createNewSalon(self):
        f = open("Salon.txt", "a")
        if self.checkCopy(self) == False:
            f.write(
                str(self.id) + ";" + str(self.location) + ";" + str(self.name) + "\n")

    def getAllSalons(self):
        f = open("Salon.txt", "r")
        lines = f.readlines()
        Salons = []
        for l in lines:
            l = l.replace("\n", "")
            l = l.split(";")
            Salons.append(l)
        f.close()
        return Salons

    def getSalonById(self, id):
        Salons = self.getAllSalons()
        for l in Salons:
            if l[0] == str(id):
                return l
            else:
                return 0

    def deleteSalon(self, id):
        f = open("Salon.txt", "r")
        Salons = self.getAllSalons()
        count = -1
        for l in Salons:
            count += 1
            if l[0] == str(id):
                Salons.pop(count)
        print(Salons)
        f.close()
        f = open("Salon.txt", "w")
        for l in Salons:
            for i in range(len(l)):
                if i == len(l) - 1:
                    f.write(l[i])
                else:
                    f.write(l[i] + ";")
            f.write("\n")

