"""
"""

import numpy as np 

class Raw_data:

    __courses = []
    __students = []
    __grades = []

    __student2Courses = {}
    __course2Students = {}

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
                    self.__grades.append(row[1:])
                    self.__student2Courses[row[0]] = row[1:]

                line = f.readline()
                pointer += 1

        f.close()

    
    def get_courses(self):
        return self.__courses
    
    def get_students(self):
        return self.__students

    def get_grades(self):
        return np.array(self.__grades)

    def get_student2Courses(self):
        return self.__student2Courses




if __name__ == "__main__":

    np.set_printoptions(threshold=np.inf, linewidth=1800)
    data = Raw_data("dataset/UQDataset_5_5639.csv")
    students = data.get_students()
    courses = data.get_courses()
    grades = data.get_grades()

    s2C = data.get_student2Courses()
    
    np.savetxt("grades.csv", delimiter= ",", header="course")
    

    # print(grades[1:10])
    print(courses)
    print(s2C.get("s0000001"))





