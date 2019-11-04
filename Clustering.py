
from Data import Data
import seaborn as sns
import sklearn as sk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_similarity_score
from sklearn.cluster import AgglomerativeClustering
from scipy.spatial.distance import pdist, jaccard
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import silhouette_score

import pandas as pd
import matplotlib.pyplot as plt



from sklearn.decomposition import PCA
data = Data("dataset/UQDataset_5_5639_m.csv")
c2s = data.get_all_course2student()
s2c = data.get_all_student2course()

df_c2s_int = pd.DataFrame(data.get_int_dataset(c2s))
df_s2c_int = pd.DataFrame(data.get_int_dataset(s2c))

# c2s_int.corr()
# df_s2c_int.corr()




pca = PCA(n_components= 0.9)
pca.fit(df_s2c_int)
reduc_s2c = pd.DataFrame(pca.transform(df_s2c_int))

pca.fit(df_c2s_int)
reduc_c2s  = pd.DataFrame(pca.transform(df_c2s_int))
reduc_c2s





corr_mat = df_s2c_int.corr()
course_distance = pairwise_distances(corr_mat, metric="correlation")

# %matplotlib notebook
sns.heatmap(corr_mat, center=0, vmin=-1, vmax=1)
plt.show()


# s2c_int = data.get_int_dataset(s2c)

# s2c_int[s2c_int != 0] = 1

# bin_s2c = pd.DataFrame(s2c_int)

# jac_sim = 1 - pairwise_distances(bin_s2c, metric="hamming")

# jac_sim = pd.DataFrame(jac_sim)    
# jac_sim




# %matplotlib notebook
# sns.heatmap(jac_sim, vmax=1, vmin=0)


# distance = 1-jac_sim
# sil_coe = []
# for n in range(2,21):
#     clustering = AgglomerativeClustering(n_clusters=n, affinity="precomputed", linkage="complete").fit(course_distance)
#     lable = clustering.labels_
#     sil_coe.append(silhouette_score(course_distance, lable))
#     print(n, sil_coe)

# n = list(range(2,21))
# plt.figure()
# plt.plot(n, sil_coe)
# plt.xlabel("number of clusters")
# plt.ylabel("sillouette coefficient mean")
# plt.show()




# from pandas.plotting import parallel_coordinates

# distance['cluster'] = pd.DataFrame(clustering.labels_)
# # get_ipython().run_line_magic('matplotlib', 'notebook')
# # parallel_coordinates(distance, 'cluster') 
# # plt.show()
# print(distance)





