from Data import *
from FPTree import *
import numpy as np  


def get_freq_courses(data, support):
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
    freq_courses = {}
    for col in range(0, data.shape[1]):
        column = data[:, col]
        count = len(column[column != 0])
        if count/data.shape[0] >= support:
            freq_courses[col] = count

    sorted_courses={}
    for k,v in sorted(freq_courses.items(), key=lambda item: item[1], reverse=True):
        sorted_courses[k] = v
    return sorted_courses
        

def get_sorted_records(data, sorted_courses):
    """
    input: 
        data(np.array): student to course.
            dtype: int64
        sorted_cources(np.aray): sorted courses index from High to Low 
            dtype: Int

    Output:
        student to course index about the freq cources.
        from high to low
    """
    sorted_record = list()
    for student in data:
        freq_course_grades = student[sorted_courses]
        #record the course index that student has grade
        sorted_record.append(sorted_courses[freq_course_grades != 0])

    return np.array(sorted_record)


# def update_FPTree(fp_tree, records):
    
#     current_node = fp_tree.get_root()
#     # print(len(current_node.get_children()))
#     for course in records:

#         child = current_node.search_child(str(course))
        
#         if child:
#             child.add_count()
#         else:
#             child = FPTree.Node(str(course), 1, current_node)
#             current_node.add_child(child)
    
#         current_node = child
                
#     return fp_tree


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

    freq_cources = get_freq_courses(trainset, 0.05)
    # get frequent course indices.
    freq_indices = np.array(list(freq_cources.keys()))
    # get frequent course indices that student has grade.
    records = get_sorted_records(trainset, freq_indices)

    fp_tree = FPTree()

    # generate FP-Tree.

    for record in records:
        fp_tree.update_tree(record)
    # # test
    root = fp_tree.get_root()
    # children = root.get_children()
    # print(len(children))
    
    print(freq_indices)
    fp_tree.print_tree("",root)