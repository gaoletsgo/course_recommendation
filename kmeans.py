from Data import *
import numpy as np  
from matplotlib import pyplot as plt 

class KMeans:

    # # data = Data("dataset/UQDataset_5_5639.csv")

    # def __init__(self, filepath):
    #     data = Data(filepath)
    #     self.__s2c_trainset = data.get_s2c_trainset()
    #     self.__c2s_trainset = data.get_c2s_trainset()

    # # random points in the range.
    # def _init_centeroid(self, k, gpa=8, courseNum=108):
    #     return np.random.randint(gpa, size=(k, courseNum))  

    def init_centeroids(self, k, int_trainset):
        centeroids = int_trainset.copy()
        np.random.shuffle(centeroids)
        return centeroids[:k]

    def get_int_grade(self, str_trainset):
        strGrade = str_trainset[...,1:]
        strGrade[strGrade==""] = "0"
        return strGrade.astype(np.int64)
    
    def get_closest_index(self, trainset, centeroids):
        dist = np.sqrt(np.square(trainset - centeroids[:, np.newaxis]).sum(axis=2))
        return np.argmin(dist, axis=0)
    
    def clustering(self, k, closest_index, trainset):
        clusters = list()
        [clusters.append(list()) for length in range(k)]

        for index in range(k):
            clusters[index] = trainset[closest_index == index]
        return clusters
    
    def get_mean(self, cluster):
        return cluster.mean(axis=0)

    def change_centeroids(self, clusters):
        new_centeroids = []
        for cluster in clusters:
            int_grade = self.get_int_grade(cluster)
            new_centeroids.append(self.get_mean(int_grade))
        return np.array(new_centeroids)

    def get_SSE(self, clusters, centeroids):
        SSE = []
        for index in range(len(centeroids)):
            int_grade = self.get_int_grade(clusters[index])
            distence = np.sqrt(np.square(int_grade - centeroids[index]).sum(axis=1))
            SSE.append(distence.sum(axis = 0))
        return np.array(SSE)

    def determine_K(self, dataset):
        sse = []
        for k_value in range(2,15):
            clusters = self.fit(k_value, trainset)
            centeroids = self.change_centeroids(clusters)
            # s = self.get_SSE(clusters, centeroids)
            sse.append(self.get_SSE(clusters, centeroids).sum(axis=0))
        x = range(2,15)
        y = sse
        plt.plot(x,y)
        plt.show()
        # diff = np.diff(np.array(sse))
        # return diff


    def fit(self, k, trainset):
        
        int_trainset = self.get_int_grade(trainset)
        centeroids = self.init_centeroids(k, int_trainset)

        centeroid_change = True
        while centeroid_change:
            centeroid_change = False
            closest_index = self.get_closest_index(int_trainset, centeroids)
            clusters = self.clustering(k, closest_index, trainset) # string traiset
            new_centeroids = self.change_centeroids(clusters)

            if (new_centeroids != centeroids).any():
                centeroid_change = True
                centeroids = new_centeroids

        # print([len(cluster) for cluster in clusters])
        return clusters




   
    #     clusters = list()
    #     [clusters.append(list()) for length in range(k)]




if __name__ == "__main__":

    data = Data("dataset/UQDataset_5_5639.csv")
    trainset = data.get_s2c_trainset()
    kmeans = KMeans()
    # kmeans.fit(4,trainset)
    # print(kmeans.determine_K(trainset))
    kmeans.determine_K(trainset)