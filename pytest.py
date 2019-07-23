import numpy as np  

a = np.array([[1,2,3],[4,5,6],[7,8,9],[11,22,33],[44,55,66],[77,88,99]])
b = np.array([[3,3,3],[4,4,4]])

dist = a-b[:,np.newaxis]
print(b.mean(axis=0))
c = np.array([1,2,3])
d = np.array([1,2,4])

print((c != d).any())
# print(np.argmin(np.square(a-b[:,np.newaxis]).sum(axis=1), axis=1))
