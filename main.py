import Procedure as p
import Salon as s
import Master as m
import User as u

a = p.Procedure()
salon = s.Salon()
master = m.Master()
user = u.User()
#print(a.getAllProcedures())
#print(a.getProcedureById("01"))
#a.deleteProcedure("06")
b = p.Procedure("01", 64, "asdsadasd", "asdasdasdasdasdadasd", 0)
c = p.Procedure("03", 6, "dsadasd", "asdasdasdasdadasd", 5)
b.createNewProcedure()
c.createNewProcedure()
print(salon.getAllSalons())
print(master.getAllMasters())
print(user.getAllUsers())
