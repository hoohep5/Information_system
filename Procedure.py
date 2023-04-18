class Procedure():
    def __init__(self, id):
        self.id = id
    id = 0
    data = 0
    name = "noname"
    description = "text"
    price = 0
    master_id = 0
    def createNewProcedure(self):
        pass
    def getAllProcedures(self):
        pass
    def getAllSorted(self):
        pass
    def getProcedureById(self, id):
        if self.id == id:
            print(self.description)
    def deleteProcedure(self):
        pass
    pass