from Data import *
from KMeansJ import *
import numpy as np  

def s2c_cluster():
    data = Data("dataset/UQDataset_5_5639.csv")
    km = KMeansJ()
    s2c = data.get_s2c_trainset()
    return km.fit(8, s2c)

def c2s_cluster():
    data = Data("dataset/UQDataset_5_5639.csv")
    km = KMeansJ()
    c2s = data.get_c2s_trainset()
    return km.fit(20,c2s)

if __name__ == "__main__":
    
    # clusters = s2c_cluster()
    # for cluster in clusters:
    #     print(len(cluster))
    np.set_printoptions(threshold=np.inf)
    clusters = c2s_cluster()
    for cluster in clusters:
        print("next cluster:", "length: ",len(cluster))
        for c in cluster:
            print(c[0])
        