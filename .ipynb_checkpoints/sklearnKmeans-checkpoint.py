from Data import *
import numpy as np
# from sklearn.cluster import KMeans
from sklearn.cluster import KMeans

data = Data("dataset/UQDataset_5_5639.csv")

s2c = data.get_s2c_trainset()


km = KMeans(n_clusters=8)
km.fit(s2c)