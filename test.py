import numpy as np

courses = []
students = []
grades = []

with open("dataset/UQDataset_5_5639.csv", "r") as f:
    line = f.readline()

    # get courses
    headers = line.split(",")
    for course in headers:
        if (course != ""):
            courses.append(course)

    # get students and gardes
    while line != "":
    
        line = f.readline()
        row = line.split(",")
        
        students.append(row[0])
        grades.append(row[1:])

f.close()


# remove '\r\n'
for grade in grades:
    last_index = len(grade)-1
    grade[last_index] = grade[last_index].strip("\r\n")
    
matrix = np.array(grades)

# print(matrix)