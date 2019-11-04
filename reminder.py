
from helper import course_code_name, course_index_code
import pickle
from itertools import combinations
from collections import OrderedDict
from Data import Data
import numpy as np

# def reminder(grades):

#     courses = grades.keys()
#     ind2code, code2ind =  course_index_code()
#     course_indices = [code2ind[c] for c in courses]

#     return course_indices




if __name__ == "__main__":
    
    # grades = {"csse7030": 6, "deco7140": 5, "infs7900": 6, "infs7202": 7, "comp7505": 4, "csse7023": 7, "deco7280": 5, "infs7903": 7}
    grades = {"deco7280": 5}
    # , ""}
    rules = pickle.load(open("temp/associate_rules.txt", "rb"))
    ind2code = pickle.load(open("temp/course_index_to_code.txt", "rb"))
    code2ind = pickle.load(open("temp/course_code_to_index.txt", "rb"))
    code2name = pickle.load(open("temp/course_code_to_name.txt", "rb"))

    indices = [code2ind[c] for c in grades.keys()]
    print(indices)

    # print(rules[frozenset(list(("63", "65")))])
    rec_list = {}
    for i in range(1, len(indices)+1):

        
        for subset in combinations(indices, i):
            try:
                # enrolled = [ind2code[c] for c in subset]
                for item in rules[frozenset(list(subset))]:
                    rec = item[0]
                    conf = item[1]

                    for c in rec:
                        if c in indices:
                            continue

                        if c not in rec_list.keys():
                            rec_list[c] = {"if_set": subset, "conf": conf}
                        elif conf > rec_list[c]["conf"]:
                            rec_list[c] = {"if_set": subset, "conf": conf}
                    
                    
            except KeyError:
                continue
    
    rec_list = OrderedDict(sorted(rec_list.items(), key=lambda item: item[1]["conf"], reverse=True))
    
    
    # do recommendation

    for rec in rec_list.items():
        
        print("Recommend to enroll {0}, because {1}% studetns who enrolled{2} also enrolled this course.".format(code2name[ind2code[rec[0]][0]], round(rec[1]["conf"]*100, 2), [code2name[ind2code[c][0]] for c in rec[1]["if_set"]]))


    # print(ind2code)

    data = Data("dataset/UQDataset_5_5639_m.csv")
    courses = data.get_courses()

    trainset = data.get_int_dataset(data.get_all_student2course())

    print(code2ind["csse7030"], code2ind["deco7280"])

    # print(len(np.where((trainset[:, 60] != 0) & (trainset[:, 104] != 0))[0]))

    # print(len(np.where(trainset[:,60] != 0)[0]), len(np.where(trainset[:, 104] != 0)[0]))

    # print(rules[frozenset(['63', '12', '28'])])
    # print(trainset)
    # for index in range(0, len(courses)):
    #     print(index, courses[index])