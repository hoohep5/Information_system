class User():
    def __init__(self, id='00', login='0', password='-', admin=0):
        self.id = id
        self.login = login
        self.password = password
        self.admin = admin

    id = "0"
    login = "0"
    password = "noname"
    admin = "text"

    def checkCopy(self, p):
        flag = False
        f = open("User.txt", "r")
        lines = f.readlines()
        UsersID = []
        for l in lines:
            l = l.replace("\n", "")
            l = l.split(";")
            UsersID.append(l)
        for i in UsersID:
            if (i[0] == p.id or i[1] == p.login or i[2] == p.password):
                flag = True
        return flag

    def createNewUser(self):
        f = open("User.txt", "a")
        if self.checkCopy(self) == False:
            f.write(
                str(self.id) + ";" + str(self.login) + ";" + str(self.password) + ";" + str(self.admin) + "\n")

    def getAllUsers(self):
        f = open("User.txt", "r")
        lines = f.readlines()
        Users = []
        for l in lines:
            l = l.replace("\n", "")
            l = l.split(";")
            Users.append(l)
        f.close()
        return Users

    def getUserById(self, id):
        Users = self.getAllUsers()
        for l in Users:
            if l[0] == str(id):
                return l
            else:
                return 0

    def deleteUser(self, id):
        f = open("User.txt", "r")
        Users = self.getAllUsers()
        count = -1
        for l in Users:
            count += 1
            if l[0] == str(id):
                Users.pop(count)
        print(Users)
        f.close()
        f = open("User.txt", "w")
        for l in Users:
            for i in range(len(l)):
                if i == len(l) - 1:
                    f.write(l[i])
                else:
                    f.write(l[i] + ";")
            f.write("\n")
