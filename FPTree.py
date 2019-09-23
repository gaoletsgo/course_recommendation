import numpy as np  
import copy
from FreqItemSet import *

class FPTree:

    class Node:

        # Non-leaf node
        def __init__(self, name="root", count=0, parent="None"):
            self.__parent = parent
            self.__node_name = str(name)
            self.__count = count
            self.__children = list()

        def get_parent(self):
            return self.__parent
        
        def add_child(self,child):
            """
            input: child(Node)

            """
            self.__children.append(child)
        
        def add_count(self):
            self.__count += 1

        def get_children(self):
            """
                return a list of children Node.
            """
            return self.__children
        
        def get_all_children_name(self):
            return [child.get_node_name() for child in self.__children]

        def search_child(self, name):
            
            for child in self.__children:
                if child.get_node_name() == str(name):
                    return child
            
            return None

        def get_node_name(self):
            return self.__node_name

        def set_count(self, count):
            self.__count = count

        def get_count(self):
            return self.__count
        
        def __str__(self):
            return str(self.__node_name)+": "+str(self.__count)

    def __init__(self):
        self.__root = self.Node()
        self.__pointer_table = {"root" : [self.__root]}
    
    def get_root(self):
        return self.__root
    
    def update_tree(self, record):

        current_node = self.get_root()

        for course in record:
            
            child = current_node.search_child(str(course))
        
            if child:
                child.add_count()
            else:
                child = FPTree.Node(str(course), 1, current_node)
                current_node.add_child(child)

                # create head point table
                name = child.get_node_name()
                if name in self.__pointer_table.keys():
                    self.__pointer_table[name].append(child)
                else :
                    self.__pointer_table[name] = [child]
        
            current_node = child
    

    # def conditional_tree(self):

    def get_prefix(self, node):
        """
            input:
                node(FPTree.Node): 
                    FP-Tree node.

            return:
                prefix(List):  
                    List of nodes. 
                    child is in the last index, 
                    ancestor is in the first index.
                    
        """
        
        prefix = []
        count = node.get_count()

        parent = node.get_parent()
        while parent is not self.__root:
            parent_node = copy.copy(parent)
            parent_node.set_count(count)
            prefix.insert(0, parent_node)

            parent = parent.get_parent()
        
        return prefix
            
    # todo: mining the frequent item set of the prefix.
    def get_prefix_freq_item_set(self, prefix, count):
        """
            Mining associate rules in one prefix.
            input: 
                prefix(list of node): A prefix of the FP-tree.
            output:
                the frequent item set in this prefix.
                pref_freq_item_set(set): FreqItemSet in set in this prefix.
        """ 
        pref_freq_item_set = set()

        if prefix == []:
            return pref_freq_item_set

        if len(prefix) == 1:
            child = set([prefix[0].get_node_name()])
            pref_freq_item_set.add(FreqItemSet(child, count))
            return pref_freq_item_set

        else :
            child = set([prefix[-1].get_node_name()])
        
            prev_item_set = self.get_prefix_freq_item_set(prefix[:-1], count)

            for s in prev_item_set:
                pref_freq_item_set.add(FreqItemSet(s.itemset|child, count))
            
            pref_freq_item_set.add(FreqItemSet(child, count))
            pref_freq_item_set = pref_freq_item_set | prev_item_set
            
            return pref_freq_item_set
    
    def _get_item_in_set(self, itemset, item):
        copy_set = copy.copy(itemset)
        # print(item in itemset)
        copy_set.remove(item)
        return itemset.difference(copy_set).pop()

    def get_freq_item_set(self, course_index, support, data_size):
        
        course_nodes = self.__pointer_table[course_index]

        course_freq_set = set()
    
        for node in course_nodes:

            count = node.get_count()

            # remove the prefix that below the support
            if count/data_size < support:
                continue

            suffix = set([node.get_node_name()])
            prefix = self.get_prefix(node)

            prefix_freq_set = self.get_prefix_freq_item_set(prefix,count)
            freq_with_suffix = set()
            # add suffix to the frequent item set.
            for pref_set in prefix_freq_set:
                pref_set.itemset = suffix
                freq_with_suffix.add(pref_set)
                
                # print(pref_set) # to be deleted.
            # print("pref set: ",len(prefix_freq_set), "mainset: ",len(course_freq_set))
         
             # add suffix itself because it is a frequent set as well.
            freq_with_suffix.add(FreqItemSet(suffix, count))

            # intersection in prefix freq itemset and main item set.
            intersection = freq_with_suffix & course_freq_set
            # print("inter", len(intersection))
            # add the count in prefix freq set to the main freq item set.
            for item in intersection:

                existed_freq_set = self._get_item_in_set(course_freq_set, item)
                existed_freq_set.count += self._get_item_in_set(freq_with_suffix, item).count
            
            # remove intersecion in prefix frequent item set.
            prefix_freq_set.difference_update(intersection)
            # add the difference set into the main set.
            course_freq_set = course_freq_set | freq_with_suffix

        return course_freq_set
            
    # def mining_assocaite_rules(self, freq_item_set):
    #     """
    #         Input: 
    #             freq_item_set: Set(FreqItemSet)
            
    #         Output: 
    #             Associate rules in a frequent item set.
    #     """






    def get_node_pointer(self):
        return self.__pointer_table


    # def print_tree(self, padding, node):
    #     content = ">"+ str(node.get_node_name())
    #     print(content, end="")
    #     padding += " "*int(len(content)/2)
    #     children = node.get_children()
    #     if children:
    #         for child in children:
    #             # print("{0}|".format(padding),end="")
    #             self.print_tree(padding, child)
    #     else:
    #         print("leaf")
    #         # print(padding+"|",end="")