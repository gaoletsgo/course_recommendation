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

            # get courses
            headers = line.split(",")
            for course in headers:
                if (course != ""):
                    self.__courses.append(course)

            # get studetns and grades.
            while line :
                line = f.readline()

                #remove \r\n
                line = line.strip("\r\n")
                row = line.split(",")
                    
                self.__students.append(row[0])
                self.__grades.append(row[1:])
                self.__student2Courses[row[0]] = row[1:]
        
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

    data = Raw_data("dataset/UQDataset_5_5639.csv")
    students = data.get_students()
    courses = data.get_courses()
    grades = data.get_grades()

    s2C = data.get_student2Courses()

    print(grades)
    print(len(s2C))
    print(s2C.get(""))





