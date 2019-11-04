from Data import Data  
import numpy as np 
import re
import plotly.express as px
import pandas as pd 
from CourseReminder import CourseReminder
import pickle
from sklearn.metrics.pairwise import pairwise_distances



data = Data("dataset/UQDataset_5_5639_m.csv")
c2s = data.get_int_dataset(data.get_all_course2student())
s2c = data.get_int_dataset(data.get_all_student2course())
# full_table = pd.DataFrame(data.get_fulltable())
s2c[(s2c<4) & (s2c>0)] = 1
s2c[(s2c<6) & (s2c>3)] = 2
s2c[s2c>5] = 3

cr = CourseReminder(0.03, 0.65).fit(s2c)
# print(list(cr.c_rec([0,45,104])))

record = np.zeros(106).astype(np.int64)
ind = np.array([2,5,7,98,1,9,10])
record[ind] = [5,7,3,6,4,5,5]
# record = record.reshape(1,-1)
print(record)
# record = np.array([record])
# dist = pairwise_distances(s2c,record)s
# s = cr.s2c()
# print(dist.reshape(1,-1))
# l = cr.student_cluster_labels_
# print(s.shape)
# l = l[:,np.newaxis]
# print(l, l.shape)
# s = np.append(s,l,axis=1)
# print(s)
# l.reshape()
# record = pd.DataFrame(record)
# # record = record.transpose()
print(cr.student_label(record))

print(record.shape)
# # print(cr.c_rec(record))
# # print(record[record!=0].index)
# r = cr.genenate_recommendation(["31", "45"], [4,6])

# g,f =cr.predict_grade([25,104],[[3,7]],31,s2c)
# print(g,f)

# a = np.array([1,2,3,4,5])
# print(set(np.where(a>3)[0]))