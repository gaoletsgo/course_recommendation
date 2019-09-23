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

def get_frequent_courses_set(fp_tree, course_indices):
    
    frequent_courses_set = set()
    node_locator = fp_tree.get_node_pointer()

    # Mining 
    for course in course_indices:
        print("Course: ", course)
        # get all nodes of course X
        node_locations = node_locator[course]   

        # get all prefix of course X
        for node in node_locations:
            prefix = fp_tree.get_prefix(node)
            freq_course_set_in_prefix = fp_tree.get_freq_item_set(prefix)
            
            for freq_set in frequent_courses_set:

                if freq_set in freq_course_set_in_prefix:

                    # get the FreqItemSet object in the prefix
                    set_copy = copy.copy(freq_course_set_in_prefix)
                    set_copy.remove(freq_set)
                    freq_set_in_prefix = freq_course_set_in_prefix.difference(set_copy).pop()
                    # add the count of the repeat set.
                    freq_set.count += freq_set_in_prefix.count

            # add difference set to the frequent_course_set.
            difference = copy.copy(freq_course_set_in_prefix)
            difference.difference_update(frequent_courses_set)

            frequent_courses_set = frequent_courses_set | difference

    return frequent_courses_set

# def get_frequent_set(fp_tree, course_indices):

#     node_locator = fp_tree.get_node_pointer()


#     for course in course_indices:

#         course_nodes = node_locator[str(course)]
        
#         for node in course_nodes:

#             prefix = fp_tree.get_prefix(node)

#             if  len(prefix) == 1:


if __name__ == "__main__":

    f=open("fp.txt", "w+")


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


# freqset mining    

    print(freq_indices.astype(str))

    # freq_set = get_frequent_courses_set(fp_tree, freq_indices.astype(np.str)[:5])

    # for s in freq_set:
    #     print(s)


    #test:

    node_locator = fp_tree.get_node_pointer()

    # nodes = node_locator["52"][0]

    # all_set = set()

    # # # for node in nodes:
        
    # prefix = fp_tree.get_prefix(nodes)
    
    # freq_set = fp_tree.get_prefix_freq_item_set(prefix,100)
    # print(type(freq_set))
    # for s in freq_set:
    #     s.itemset = set(["qq"])
    #     all_set.add(s)
    


    # for s2 in all_set:
    #     print(s2 in all_set)


    # all_set = all_set | freq_set

    # inter = all_set & freq_set

    # for i in inter:
    #     print(fp_tree._get_item_in_set(all_set, i))


 

    
    # Mining all frequent item set:
    
    for course_index in freq_indices:
        freq_set = fp_tree.get_freq_item_set(str(course_index),0.05,trainset.shape[1])
        f.write(str(course_index)+" start : \n")
        print(course_index)
        for s in freq_set:
            f.write(str(s)+"\n")
    
    print("end")