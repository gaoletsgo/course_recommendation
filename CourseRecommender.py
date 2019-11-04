
from Data import Data
from FPGrowth import FPGrowth
from FPTree import FPTree
import numpy as np
from collections import OrderedDict
import pickle
import pandas as pd 
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import silhouette_score
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from itertools import combinations
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier

class CourseRecommender:

    def __init__(self, min_sup, min_conf):
        self.__min_sup = min_sup
        self.__min_conf = min_conf

    def fit(self, trainset):
        sorted_indices = self.__get_sorted_frequent_item_index(self.__min_sup, trainset)
        sorted_record = self.__get_sorted_records(sorted_indices, trainset)

        self.__FPGrowth = FPGrowth(trainset, self.__min_sup, self.__min_conf, sorted_record)

        init_tree = self.__FPGrowth.get_fp_tree()
        head_table = init_tree.header_table
        # frequent course set
        self.__frequent_itemset = self.__FPGrowth.frequent_itemset(head_table)
        # association rules
        self.__rules = self.__FPGrowth.associate_rules(self.__frequent_itemset)

       
        self.__c2s = trainset.transpose()
        self.__c2s = pd.DataFrame(self.__c2s)
        # clustering courses.
        self.__course_distance = pd.DataFrame(pairwise_distances(pd.DataFrame(trainset).corr(), metric="correlation"))
        # find best k in course clustering.
        self.__course_clustering = self.__best_clustering(self.__course_distance)[1]
        self.__course_cluster_labels = self.__course_clustering.labels_
        self.__course_distance["labels"] = self.__course_cluster_labels
        self.__c2s["labels"] = self.__course_cluster_labels
        
        self.course_corr = pd.DataFrame(trainset).corr()
        self.course_corr["labels"]  = self.__course_cluster_labels
       

        #  # PCA reduce dimension.
        # pca = PCA(n_components= 0.8)
        # pca.fit(pd.DataFrame(trainset).corr())
        # self.__reduc_s2c = pd.DataFrame(pca.transform(pd.DataFrame(trainset).corr()))
        # self.__reduc_s2c["labels"] = self.__course_cluster_labels

        # self._s2c = trainset
        # self._s2c = pd.DataFrame(self._s2c)
        #clustering student.
        self.__bin_dataset = self.binary_dataset(trainset)
        self.__student_distance = pd.DataFrame(pairwise_distances(self.__bin_dataset, metric="hamming"))
        self.__student_clustering = AgglomerativeClustering(n_clusters=90, affinity="precomputed", linkage="average").fit(self.__student_distance)
        self.__student_cluster_labels = self.__student_clustering.labels_
        self.__s2c = pairwise_distances(self.binary_dataset(trainset), metric="hamming")
        label = self.__student_cluster_labels[:, np.newaxis]
        # label.reshape(5649,1)
        self.__s2c =  np.append(self.__s2c,label,axis=1)
        # self.__student_distance["labels"] = self.__student_cluster_labels


        # pca = PCA(n_components= 0.8)
        # pca.fit(pd.DataFrame(trainset))
        # self.__student_distance = pd.DataFrame(pca.transform(pd.DataFrame(trainset)))

        self.__student_distance["labels"] = self.__student_clustering.labels_
        # self._s2c["labels"] = self.__student_cluster_labels

  


        return self

    def s2c(self):
        return self.__s2c

    def s_rec(self, record):
        new_record = record
        new_record[new_record != 0] = 1
        new_record = new_record.reshape(1,-1)
        dist = pairwise_distances(self.__bin_dataset, new_record)
        dist = dist.reshape(1,-1)

        x = self.__s2c[:,:-1]
        y = self.__s2c[:,-1]

        # best_k = 3
        # best_score = 0
        # for n in range(3,50):
        #     x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.25)
        #     knn = KNeighborsClassifier()
        #     knn.fit(x_train, y_train)
        #     score = knn.score(x_test, y_test)
        #     if score > best_score:
        #         best_score = score
        #         best_k = n

        high_knn=KNeighborsClassifier(32).fit(x, y)

        label =  high_knn.predict(dist)

        students = self.__student_cluster_labels[self.__student_cluster_labels  == label]

        c_list = set()
        for s in  students:
            r = np.array(self.__bin_dataset)[s]
            c = set(np.where(r[r!=0])[0])
            c_list = c_list | c
        return c_list
        # return best_k




    @property
    def student_distance(self):
        return self.__student_distance
    @property
    def course_distance(self):
        # return self.__course_distance
        return self.__course_distance
    @property
    def frequent_itemset(self):
        return self.__frequent_itemset

    def __best_clustering(self, distance):
        best_sil_coe = 0
        best_k = 3
        best_clustering = None 
        for n in range(3, int(len(distance)*0.5)):
            clustering = AgglomerativeClustering(n_clusters=n, affinity="precomputed", linkage="average").fit(distance)
            labels = clustering.labels_
            sil_coe = silhouette_score(distance, labels, metric="precomputed")
            if sil_coe > best_sil_coe:
                best_sil_coe = sil_coe
                best_k = n
                best_clustering = clustering
        return best_k, best_clustering
    
    def binary_dataset(self, dataset):
        d = dataset
        d[d!=0] = 1
        return pd.DataFrame(d)

    def genenate_recommendation(self, enrols, grades):
        # rules recom
        r_rec = {}
        for i in range(1, len(enrols)+1):
            for subset in combinations(enrols, i):
                try:
                    for item in self.__rules[frozenset(list(subset))]:
                        rec = item[0]
                        conf = item[1]
                        
                        for c in rec:
                            if c in enrols:
                                continue
                            
                            if c not in r_rec.keys():
                                r_rec[c] = {"if_set": subset, "conf": conf}
                            elif conf > r_rec[c]["conf"]:
                                r_rec[c] = {"if_set": subset, "conf": conf}
                except KeyError:
                    continue
        
        return r_rec

    def c_rec(self, enrols):
        c_rec = []
        for e in enrols:
            label = self.__c2s.iloc[e, -1]

            c_rec += list(self.__c2s[self.__c2s["labels"] == label].index.tolist())
            if e in c_rec:
                c_rec.remove(e)

        return c_rec
            

        



    
    def predict_grade(self, enrols, grades, target, dataset):

        # scale 
        scaled_grades = []
        for g in grades:
            for l in g:
                if l == 1:
                    scaled_grades.append(1)
                else:
                    scaled_grades.append(int(l/2))
        scaled_grades = np.array([scaled_grades])
        # enrols.append(target)
        ds = dataset
        for c in enrols:
            ds = ds[ds[:,c] !=0]
        ds = ds[ds[:,target]!=0]
        
        x = ds[:,enrols]
        y = ds[:, target]
        y_set = set(y)
        # print(ds, x, y, scaled_grades)
        x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.25)
        clf = MultinomialNB().fit(x_train, y_train)
      
        # print("c",clf.class_count_)
        # grades.reshape(1,-1)
        return max(clf.predict_proba(scaled_grades)[0]),clf.predict(scaled_grades)[0]



    @property
    def course_cluster_labels_(self):
        return self.__course_cluster_labels

    @property
    def student_cluster_labels_(self):
        return self.__student_cluster_labels
    
    @property
    def associate_rules(self):
        return self.__rules


    def __get_sorted_frequent_item_index(self, min_sup, data):
        """

        @param: data(np.array[int64]): student to course.  
        @param: min_sup: min support.  
        @return:  a sorted frequent item index in 'data'.
            key: course index
            value: the number of students that enrolled this course.
        """
        freq_items_index = {}
        for col in range(0, data.shape[1]):
            column = data[:, col]
            count = len(column[column != 0])
            if count/data.shape[0] >= min_sup:
                freq_items_index[col] = count

        sorted_index={}
        for k,v in sorted(freq_items_index.items(), key=lambda item: item[1], reverse=True):
            sorted_index[k] = v
        return np.array(list(sorted_index.keys()))

    def __get_sorted_records(self, sorted_item_index, data):
        """
        @param: sorted_item_index(np.array[int64]): a sorted frequent item index
        @return: 

        Output:
            student to course index about the freq cources.
            from high to low
        """

   
    
    # sorted_record = list()
    # for r in data:
    #     freq_course_grades = r[sorted_item_index]
    #     #record the course index that student has grade
    #     sorted_record.append(sorted_item_index[freq_course_grades != 0])

        return np.array([sorted_item_index[r[sorted_item_index] != 0] for r in data])




    # process data:

   

    # indices = get_sorted_frequent_item_index(0.05, trainset)
    # print(indices)

    # sorted_record = get_sorted_records(indices, trainset)  
    # # print(sorted_record)  

    # fpg = FPGrowth(trainset, 0.05, 0.5, sorted_record)


    # init_tree = fpg.get_fp_tree()

    # ht = init_tree.header_table

    # # for elem in ht.items():
    # #     print(elem[0], elem[1]["count"], len(elem[1]["nodes"]))

    # frequent_itemset = fpg.frequent_itemset(ht)
    # print(frequent_itemset[frozenset(["60", "104"])])
    # rules = fpg.associate_rules(frequent_itemset)
    # pickle.dump(rules, open("associate_rules.txt", "wb"))

    # # for r in rules:
    # #     print(list(r["if_set"])," ==>> ", list(r["then_set"]), r["confidence"])
    
    # # print(len(rules))
    # # for i in frequent_itemset.items():
    # #     print(list(i[0])," count: " ,i[1])
    # # print(len(frequent_itemset))

    # # print(frequent_itemset[frozenset(["6"])])

    # courses = data.get_courses()

    # print(courses[37], courses[60], courses[58], "->", courses[24], courses[39], courses[40], courses[15])
    # print(rules[frozenset(['60'])])

    