import numpy as np  
import re



a=np.array([[1,1,5],[2,1,3],[1,1,4]])
col = a[:,0:2]

print(col)

print((a[:,0]==1) & (a[:,1]==1))
print(None in [])
