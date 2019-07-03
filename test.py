import numpy as np

np.set_printoptions(threshold=np.inf, linewidth=1000)


path = "dataset/UQDataset_5_5639.csv"

data = np.genfromtxt(path, delimiter=",",dtype=None)

courses = np.array([data[0][1:]])

students = np.array([[row[0] for row in data[1:]]])


grades = np.array([row[1:] for row in data[1:]])
grades[grades == ""] = 0

print(courses)
print(np.transpose(students))
# print(grades)

print(type(grades[0][0]))   
print(grades[0][0] )

students
