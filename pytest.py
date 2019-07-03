import numpy as np 
import matplotlib.pyplot as pt 

a = np.array([1,1,1,1,1,1])
b = np.array([2,2,2,2,2,2])
c = np.array([3,3,3,3,3,3])

print(a.dtype)

# print(a.transpose())

pt.quiver(a,b,c)
pt.show()