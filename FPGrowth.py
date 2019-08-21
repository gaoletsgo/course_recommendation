from Data import *
from FPTree import *
import numpy as np  


def get_head_point_table(data, support):
    """
    input: 
        data(np.array): student to course.
            dtype: int64
            shape(4000, 108)
        support: min support.

    output:    
        a sorted dictionary. 
        key: course index
        value: the number of students that enrolled this course.
    """
    
    hpt = {}
    for col in range(0, data.shape[1]):
        column = data[:, col]
        count = len(column[column != 0])
        if count/data.shape[0] >= support:
            hpt[col] = count

    sorted_hpt={}
    for k,v in sorted(hpt.items(), key=lambda item: item[1], reverse=True):
        sorted_hpt[k] = v
    return sorted_hpt
         
def update_FPTree(fp_tree, record, course_indices):
    
    current_node = fp_tree.get_root()
    # print(len(current_node.get_children()))
    for index in course_indices:

        if record[index] != 0:

            children = current_node.get_children()
            
            if index == 82 and current_node is fp_tree.get_root():
                print(len(children))

            # if the node has no children
            if len(children) == 0:
                new_node = FPTree.Node(index, 1, current_node)
                current_node.add_child(new_node)
                current_node = new_node
                continue
            
            child = current_node.search_child(str(index))
                

            if child in children:
                child.add_count()
                current_node = child
             
            else:
                new_node = FPTree.Node(index, 1, current_node)
                current_node.add_child(new_node)
                current_node = new_node
                    
    return fp_tree


def print_FPTree(fp_tree):
    current_node = fp_tree.get_root()
    print(current_node)
    children = current_node.get_children()
    for child in children:
        print(child)



if __name__ == "__main__":

    data = Data("dataset/UQDataset_5_5639.csv")
    trainset = data.get_int_dataset(data.get_s2c_trainset())
  


    np.set_printoptions(linewidth=np.inf, threshold=np.inf)

    hpt = get_head_point_table(trainset, 0.05)
    course_indices = np.array(list(hpt.keys()))
    print(course_indices)

    index_trainset = trainset[:,course_indices]
    # print(index_trainset[:,1])
    print(len(index_trainset[index_trainset[:,0] != 0]))
    print(len(index_trainset[(index_trainset[:,0] == 0) & \
        (index_trainset[:,1] != 0)]))
    print(len(index_trainset[(index_trainset[:,0] == 0) & \
            (index_trainset[:,1] == 0) &\
                index_trainset[:,2] != 0]))
 
    

    # print(trainset[0][course_indices])

    fp_tree = FPTree()

    for record in trainset:
 
        fp_tree = update_FPTree(fp_tree,record,course_indices)
       
    # # print tree
    current_node = fp_tree.get_root()
    children = current_node.get_children()    
    print(len(children))