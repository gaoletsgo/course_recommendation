"""
k-means
"""
from Raw_data import *
import numpy as np 



if __name__ == "__main__":


    data = Raw_data("dataset/UQDataset_5_5639.csv")

    grades = data.get_grades()
    s2C = data.get_student2Courses()

    students = data.get_students()
    # print(students)
    # determine origin cluster center   

    cluster = [[],[],[],[]]
    cluster_cent = np.random.randint(8, size=(4,108))


    
    for s2c_grade in students:
        grade = np.array(s2c_grade[1:])
        grade[grade == ""] = 0
        grade = grade.astype(np.int64)
        
        # minDistance = np.inf
        dist = []
        # print("distance: ")
        for center in cluster_cent:

            distance = np.linalg.norm(grade - center)

            dist.append(distance)
            
        # print("min distance: ",min(dist), "index: ",dist.index(min(dist)))

        index = dist.index(min(dist))

        cluster[index].append(s2c_grade)


        for center in cluster_cent:
            

   


        
