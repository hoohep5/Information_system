class Procedure():
    def __init__(self, id = '00', data = '0', name = '-', description = '-', price = '0'):
        self.id = id
        self.data = data
        self.name = name
        self.description = description
        self.price = price
    id = "0"
    data = 0
    name = "noname"
    description = "text"
    price = 0
    master_id = 0

    def checkCopy(self, p):
        flag = False
        f = open("Procedure.txt", "r")
        lines = f.readlines()
        ProceduresID = []
        for l in lines:
            l = l.replace("\n", "")
            l = l.split(";")
            ProceduresID.append(l)
        for i in ProceduresID:
            if (i[0] == p.id or i[1] == p.data or i[2] == p.name or i[3] == p.description or i[4] == p.price):
                flag = True
        return flag

    def createNewProcedure(self):
        f = open("Procedure.txt", "a")
        if self.checkCopy(self) == False:
            f.write(str(self.id) + ";" + str(self.data) + ";" + str(self.name) + ";" + str(self.description) + ";" + str(
            self.price) + "\n")
    def getAllProcedures(self):
        f = open("Procedure.txt", "r")
        lines = f.readlines()
        Procedures = []
        for l in lines:
            l = l.replace("\n", "")
            l = l.split(";")
            Procedures.append(l)
        f.close()
        return Procedures
    def getProcedureById(self, id):
        Procedures = self.getAllProcedures()
        for l in Procedures:
            if l[0] == str(id):
                return l
            else:
                return 0
    def deleteProcedure(self, id):
        f = open("Procedure.txt", "r")
        Procedures = self.getAllProcedures()
        count = -1
        for l in Procedures:
            count+=1
            if l[0] == str(id):
                Procedures.pop(count)
        print(Procedures)
        f.close()
        f = open("Procedure.txt", "w")
        for l in Procedures:
            for i in range(len(l)):
                if i == len(l)-1:
                    f.write(l[i])
                else:
                    f.write(l[i] + ";")
            f.write("\n")