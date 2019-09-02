import numpy as np  
from FPTree import *
import copy
from functools import reduce
from Data import *

from FreqItemSet import *
f=open("result.txt","w+")

class Obj:

        def __init__(self, value):
                self.__value = value


        @property
        def value(self):
                return self.__value




a = FPTree.Node("1",1,"root")

b = FPTree.Node("2",1,"root")

c = FPTree.Node("3",1,"63")

d = FPTree.Node("4", 1, "53")

a2 = copy.copy(a)
a3 = a

dic1 = {"a": [a,b], "b" : [c,d]}
dic2 = {"b" : [b,c]}

def get_index(*indices):
    return reduce(np.intersect1d, indices)

ds = np.random.randint(0,10,size=[10,10])
print(ds)
# print(ds[:,1])

c = np.array([0,1,2])
print(ds[:,c])

index1 = np.any(ds[:,c] == 0, axis=1)
# index2 = np.where(ds[:,1]>5)
# index3 = np.where(ds[:,2]>5)
print(index1)
# index = get_index(index1,index2,index3)
# print(index1, index2, index3, index)


# print(ds[index and index2])


itset = FreqItemSet(set(["1", "2","3"]), 1)

itset2 = FreqItemSet(set(), 2)

i3 = FreqItemSet(set(["1", "2","3"]), 3)

fp = FPTree()

data = Data("dataset/UQDataset_5_5639.csv")



s1 = {itset}
s2 = {itset2, i3}

s3 = s1 | s2

inter = s3&s1

print(i3 in s2, hash(i3))
for i in s2:
        f.write(str(hash(i))+"\n")
        f.write("write")
        print(hash(i))

i3.itemset = set(["qq"])

print(i3 in s2, hash(i3))
for s in s2:
        print(hash(s))

# item = fp._get_item_in_set(s2, i3)

# for s in s3:
#         print(s)
#         cp = copy.copy(s2)
#         cp.remove(s)
#         print(s2.difference(cp).pop() in s2)

# print(item)

# for s in s1:

#     if s in s2:

#         s2_copy = copy.copy(s2)
#         s2_copy.remove(s)

#         s_in_s2 = s2.difference(s2_copy).pop()
#         print(s_in_s2)


# print(s2,n2)
# print(["1","2","3"] == ["1","2","3"])
# print(itset.itemset == itset2.itemset)



