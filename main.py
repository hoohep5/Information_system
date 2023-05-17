import Procedure as p
import Salon as s
import Master as m
import User as u

def login():
    print("Input login and password")

def register():
    print("Input login and password")

procedure = p.Procedure()
salon = s.Salon()
master = m.Master()
user = u.User()
print(procedure.getAllProcedures())
print(salon.getAllSalons())
print(master.getAllMasters())
print(user.getAllUsers())
comand = 0
comand = input()
if comand == 0:
    exit()
elif comand == 1:
    login()
elif comand == 2:
    register()