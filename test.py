
from Data import Data
import pickle

data = Data("dataset/UQDataset_5_5639_m.csv")

trainset = data.get_int_dataset(data.get_all_student2course())



model = pickle.load(open("temp/model.txt", "rb"))

c = model.course_distance.sort_values(by=["labels"])
s = model.student_distance.sort_values(by=["labels"])

f=open("freq.txt", "w")
f2 = open("rule.txt", "w")
freq = model.frequent_itemset
rule = model.associate_rules

for i in freq.items():
    f.write("frequent item set: "+str(set(i[0])))
    f.write("   count: "+str(i[1])+"\n")


for j in rule.items():
    f2.write("IF set: "+str(set(j[0]))+"  THEN set: "+str(set(j[1][0][0]))+"  CONFIDENCE: "+str(j[1][0][1])+"\n")

print(len(freq))
print(len(rule))
