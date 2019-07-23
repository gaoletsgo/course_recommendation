import numpy as np  


class Data:

    def __init__(self, filepath):
        
        self.__full_table = np.genfromtxt(filepath, dtype=None, delimiter=",")
    

    def get_courses(self):
        return self.__full_table[0][1:]

    def get_students(self):
        return self.__full_table[..., 0][1:]

    def get_all_student2course(self):
        return self.__full_table[1:]

    def get_s2c_trainset(self):
        all_s2c = self.get_all_student2course()
        return all_s2c[:int(0.7*len(all_s2c))]

    def get_s2c_testset(self):
        all_s2c = self.get_all_student2course()
        return all_s2c[int(0.7*len(all_s2c)):]

    def get_all_course2student(self):
        return np.transpose(self.__full_table[..., 1:])
    
    def get_c2s_trainset(self):
        all_c2s = self.get_all_course2student()
        return all_c2s[:int(0.7*len(all_c2s))]

    def get_c2s_testset(self):
        all_c2s = self.get_all_course2student()
        return all_c2s[int(0.7*len(all_c2s)):]
    