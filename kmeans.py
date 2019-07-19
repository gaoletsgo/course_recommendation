"""
K-menas
"""

from Raw_data import *
import numpy as np 

def initCenteroid(k, gpa=8, courseNum=108):
    return np.random.randint(gpa, size=(k, courseNum))

def KMmeans(data):

    def _initCenteroid(k, gpa=8, courseNum=108):
        return np.random.randint(gpa, size=(k, courseNum))

    def _getIntGrade(studentRow):
        strGrade = np.array(studentRow[1:])
        strGrade[strGrade==""] = 0 # replace no grade to 0.
        return strGrade.astype(np.int64)

    def _changeCenteroids(clusters):
        newCenteroids=np.zeros((k,108), dtype=np.int64)
        for cluster, i in zip(clusters, range(k)):
            grades = [_getIntGrade(student) for student in cluster]
            newCenteroids[i] = _getMean(grades)
        
        return newCenteroids
            
    def _getMean(listOfGrade):
        sum = np.zeros(108, dtype=np.int64) 
        for grade in listOfGrade:
            sum += grade
        
        return sum/len(listOfGrade)

    def _getSSE(clusters, centeroids):
        sum = float(0)
        for cluster,centeroid in zip(clusters,centeroids):
            grades = [_getIntGrade(student) for student in cluster]
            for grade in grades:
                sum += np.square(np.linalg.norm(grade - centeroid))

        return sum



    students = data.get_students()
     
    file = open("result.txt", "w")
    # k = 4
    for k in range(4, 40):

        for times in range(10):

    
            centeroids = _initCenteroid(k)
            # print("init centeroid: ", centeroids)


            clusters = list()
            [clusters.append(list()) for lenth in range(k)]
            # print("init clusters:", clusters)

            clusterChange = True
            while clusterChange:
                clusterChange = False

                clusters = list()
                [clusters.append(list()) for lenth in range(k)]

                for s2cGrade in students:
                    grade = _getIntGrade(s2cGrade)

                    minDist, minIndex = np.inf, -1

                    for centeroid, i in zip(centeroids, range(k)):

                        dist = np.linalg.norm(grade - centeroid)

                        if dist < minDist:
                            minDist, minIndex = dist, i

                    clusters[minIndex].append(s2cGrade)
                    # print([len(s) for s in clusters])

                if not (centeroids == _changeCenteroids(clusters)).all():
                    clusterChange = True
                    centeroids = _changeCenteroids(clusters)
                # print("new centeroids:", centeroids)

            lenth = [len(s) for s in clusters]
           
            file.write("times: "+str(times)+"\n")
            file.write(str(lenth)+"\n")
            sse = _getSSE(clusters, centeroids)
            file.write("sse: "+sse+"")

            print("write")

            # print ("times: ",times)
            # print([len(s) for s in clusters])

            # sse = _getSSE(clusters, centeroids)
            # print("sse: ", sse)


    file.close()





if __name__ == "__main__":

    data = Raw_data("dataset/UQDataset_5_5639.csv")

    initcenteroid = initCenteroid(4)

    KMmeans(data)
