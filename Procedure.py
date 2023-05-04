class Procedure():
    def __init__(self, id, data, name, description, price):
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
    def createNewProcedure(self):
        f = open("Procedure.txt", "a+")
        lines = f.readlines()
        for l in lines:
            if l != str(self.id)+";"+str(self.data)+";"+str(self.name)+";"+str(self.description)+";"+str(self.price)+"\n":
                f.write(str(self.id)+";"+str(self.data)+";"+str(self.name)+";"+str(self.description)+";"+str(self.price)+"\n")
            else:
                pass
        f.close()
    def getAllProcedures(self):
        f = open("Procedure.txt", "r")
        lines = f.readlines()
        for l in lines:
            print(l.strip())
        f.close()
    def getAllSorted(self):
        pass
    def getProcedureById(self, list ,id):
        for i in range(len(list)):
            if list[i].id == id:
                print(list[i].description + "\nprice: " + str(list[i].price))
    def deleteProcedure(self):
        pass
    def checkProcedures(self):
        pass