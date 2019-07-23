"""
"""

import numpy as np 

class Raw_data:

    __courses = []
    __students = []
    __grades = []

    __student2Courses = []
    __course2Students = []

    def __init__(self, file_path):

        
        with open(file_path,"r") as f:
            line = f.readline()
            pointer = 1

            while line != "":
                #remove \r\n
                line = line.strip("\r\n")
                
                # get courses
                if (pointer == 1):
                    headers = line.split(",")
                    for course in headers:
                        if (course != ""):
                            self.__courses.append(course)
                else :   # get studetns and grades.
                    row = line.split(",")
                    self.__students.append(row[0])

                    self.__student2Courses.append(row)
                    #Todo: get course2sudents.

                line = f.readline()
                pointer += 1

        f.close()


    def get_courses(self):
        return np.array(self.__courses, dtype=np.str)
    
    def get_students(self):
        return np.array(self.__students, dtype=np.str)

    def get_all_student2Courses(self):
        return self.__student2Courses

    # def get_s2c_trainSet(self):

    #Todo
    def get_course2Student(self):
        return 0


if __name__ == "__main__":

    data = Raw_data("dataset/UQDataset_5_5639.csv")

    print("students: {0}".format(data.get_students()))
    print("courses: {0})".format(data.get_courses()))
    print("s2c: {0}".format(data.get_all_student2Courses()))


