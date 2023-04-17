class DataBase():
    def __init__(self):
        pass
    def add_cont(self, cont):
        pass

class Container():
    def __init__(self, name, count_table, number_operation):
        self.name = name
        self.count_table = count_table
        self.number_operation = number_operation
    name = "no name"
    count_table = 0
    number_operation = 0
    matrix = [[count_table], [number_operation]]
    def fill_matrix(self):
        for i in range(2):
            for j in range(self.count_table):
                self.matrix[i][j] = 1
            for k in range(self.number_operation):
                self.matrix[i][k] = 1
    def print_info(self):
        print(self.name)
        for i in range(2):
            for j in range(self.count_table):
                print(self.matrix[i][j])
            for k in range(self.number_operation):
                print(self.matrix[i][k])
        print(self.matrix)

a = Container("NewOne", 5, 5)
a.fill_matrix()
a.print_info()
input()