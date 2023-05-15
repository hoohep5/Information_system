class Master():
    def __init__(self, id='00', describtion='none', name="none"):
        self.id = id
        self.describtion = describtion
        self.name = name

    id = 0
    describtion = "none"
    name = "no name"

    def checkCopy(self, p):
        flag = False
        f = open("Master.txt", "r")
        lines = f.readlines()
        MasterID = []
        for l in lines:
            l = l.replace("\n", "")
            l = l.split(";")
            MasterID.append(l)
        for i in MasterID:
            if (i[0] == p.id or i[1] == p.describtion or i[2] == p.name):
                flag = True
        return flag

    def createNewMaster(self):
        f = open("Master.txt", "a")
        if self.checkCopy(self) == False:
            f.write(
                str(self.id) + ";" + str(self.describtion) + ";" + str(self.name) + "\n")

    def getAllMasters(self):
        f = open("Master.txt", "r")
        lines = f.readlines()
        Masters = []
        for l in lines:
            l = l.replace("\n", "")
            l = l.split(";")
            Masters.append(l)
        f.close()
        return Masters

    def getMasterById(self, id):
        Masters = self.getAllMasters()
        for l in Masters:
            if l[0] == str(id):
                return l
            else:
                return 0

    def deleteMaster(self, id):
        f = open("Master.txt", "r")
        Masters = self.getAllMasters()
        count = -1
        for l in Masters:
            count += 1
            if l[0] == str(id):
                Masters.pop(count)
        print(Masters)
        f.close()
        f = open("Master.txt", "w")
        for l in Masters:
            for i in range(len(l)):
                if i == len(l) - 1:
                    f.write(l[i])
                else:
                    f.write(l[i] + ";")
            f.write("\n")

