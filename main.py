import Procedure as p
fProc = open("Procedure.txt", "r")
procedures = fProc.readlines()
for line in range(len(procedures)):
    procedures[line] = procedures[line].replace("\n", "")
    procedures[line] = procedures[line].split("-")
for line in range(len(procedures)):
    print(procedures[line])
proceduresEcz = []
for line in range(len(procedures)):
    proceduresEcz.append(p.Procedure(procedures[line][0],procedures[line][1],procedures[line][2],procedures[line][3],procedures[line][4]))
for line in range(len(proceduresEcz)):
    print(proceduresEcz[line].id)