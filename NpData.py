
import numpy as np 
import matplotlib.pyplot as plt 


class NpData:

    def __init__(self, path):
        data = np.genfromtxt(path, dtype=None, delimiter=",")
        self.__courses = np.array([data[0][1:]])
        self.__students = np.array([[row[0] for row in data[1:]]])
        self.__grades = np.array([row[1:] for row in data[1:]]) 

    def get_students(self):
        return self.__students
    
    def get_courses(self):
        return self.__courses

    def get_S2Cgrades(self):
        self.__grades[self.__grades == ""] = 0
        return self.__grades.astype("int_")

    def get_C2Sgrades(self):
        return self.__grades.transpose().astype("int_")



if __name__ == "__main__":

    np.set_printoptions(threshold=np.inf, linewidth=1000)

    npdata = NpData("dataset/UQDataset_5_5639.csv")

    students = npdata.get_students()
    courses = npdata.get_courses()
    s2Cgrades = npdata.get_S2Cgrades()

    c2S = npdata.get_C2Sgrades()


    distance = []

    for s in s2Cgrades:
        for s2 in s2Cgrades:

            if(s.all() != s2.all()):
                distance.append(np.linalg.norm(s,s2))
    
    print(distance)

