from Data import Data  
import numpy as np 
import re
import plotly.express as px
import pandas as pd 
from CourseRecommender import CourseRecommender
import pickle



def course_code_name(filepath):

    f = open(filepath, "r")
    courses = {}
    for line in f:
        record = line.split(",")
        course_code = record[0].split("_")

        for c in course_code:
            courses[c] = record[1]
    f.close()
    pickle.dump(courses, open("temp/course_code_to_name.txt", "wb"))
    # return courses

def course_index_code():

    data = Data("dataset/UQDataset_5_5639_m.csv")

    courses = data.get_courses()
    course_ind2code = {}
    course_code2ind = {}
    for index in range(0,len(courses)):
        course_codes = courses[index].split("_")
        course_ind2code[str(index)] = course_codes
        for code in course_codes:
            course_code2ind[code] = str(index)
    pickle.dump(course_ind2code, open("temp/course_index_to_code.txt", "wb"))
    pickle.dump(course_code2ind, open("temp/course_code_to_index.txt", "wb"))
    # return course_ind2code, course_code2ind








if __name__ == "__main__":

    data = Data("dataset/UQDataset_5_5639_m.csv")
    c2s = data.get_int_dataset(data.get_all_course2student())
    s2c = data.get_int_dataset(data.get_all_student2course())
    # full_table = pd.DataFrame(data.get_fulltable())

    cr = CourseRecommender(0.03, 0.65).fit(s2c)

    # print(len(cr.associate_rules))
    course_distance = cr.course_distance
    student_distance = cr.student_distance  
    rules = cr.associate_rules
    frequent_itemset = cr.frequent_itemset
    # print(len(rules))

    # ind = pd.Index(student_distance["labels"], name="labels")
    # a=ind.value_counts()
    # r = cr.genenate_recommendation(["27"],[6])
    # print(r)
    
    # enrols = np.array([60,104])
    # g = np.array([[2,3]])

    # c = cr.predict_grade(enrols,g,11,s2c)
    # print(c)




    pickle.dump(course_distance, open("temp/course_distance.txt", "wb"))
    pickle.dump(student_distance, open("temp/student_distance.txt", "wb"))
    pickle.dump(rules, open("temp/associate_rules.txt", "wb"))
    pickle.dump(frequent_itemset, open("temp/frequent_itemset.txt", "wb"))
    pickle.dump(cr, open("temp/model.txt","wb"))
    course_index_code()
    course_code_name("dataset/CourseName_m.csv")
    print("done")











