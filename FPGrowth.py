
import numpy as np

from FPTree import FPTree
from TreeNode import TreeNode
from ItemSet import ItemSet
from collections import OrderedDict
from itertools import combinations


class FPGrowth:
    
    def __init__(self, data, min_sup, min_conf, sorted_record):
        self.__data = data
        self.__min_sup = min_sup
        self.__min_conf = min_conf
        self.__min_count = len(data) * min_sup
        self.__fp_tree = FPTree(sorted_record, self.__min_count)

    def get_fp_tree(self):

        return self.__fp_tree

    
    
    def conditional_tree_header_table(self, item, header_table):
        """Generate a conditional fp tree for item X.
        
        Arguments:
            item {String} -- Item index
        
        Returns:
            Dict -- key: item index;
                    value: dict(count: , nodes:)
        """
        item_nodes = header_table[str(item)]["nodes"]

        root = TreeNode("root", "None")
        header_table  = {}
        for node in item_nodes:
            current_node = root
            count = node.count
            # print("count:", count)
            record = self.__fp_tree.get_prefix(node)[0]
            # print(record)
            for item in record:

                if str(item) in  header_table.keys():
                    header_table[str(item)]["count"] += count
                else:
                    header_table[str(item)] = {"count": count, "nodes": []}

                if str(item) in current_node.children.keys():
                    child_node = current_node.children[str(item)]
                    child_node.add_count(count)
                    current_node = child_node
                else:
                    new_child= TreeNode(str(item), current_node, count)
                    current_node.children[str(item)] = new_child

                    header_table[str(item)]["nodes"].append(new_child)
                    current_node = new_child
        
        header_table = OrderedDict(sorted(header_table.items(), key=lambda item: item[1]["count"], reverse=True))

        # remove unfrequent item in header table.
        for item in header_table.copy().items():
            if item[1]["count"] < self.__min_count:
                header_table.pop(item[0])
        return header_table



    def frequent_itemset(self, header_table):
        """Mining fp tree to get frequent itemset.
        
        Arguments:
            header_table {dict} -- header table. key(string): item; value: dict["count": , "nodes": ]
        
        Returns:
            dict -- key: frozenset() itemset.;
                    value: count.
        """
        items = list(header_table.keys())
        items.reverse()
        frequent_itemset = {}

        if len(items) == 1:
            frequent_itemset[frozenset([items[-1]])] = header_table[str(items[-1])]["count"]
        else:

            for item in items:
               
                pattern_base = self.frequent_itemset(self.conditional_tree_header_table(item, header_table))
                for pb in pattern_base.items():
                 
                    frequent_itemset[frozenset(list(pb[0]) + [item])] = pattern_base[pb[0]] 
                
                frequent_itemset[frozenset([item])] = header_table[str(item)]["count"]
                frequent_itemset = {**frequent_itemset, **pattern_base}

            
                
        return frequent_itemset



    def associate_rules(self, frequent_itemset):

        rules = {}

        for elem in frequent_itemset.items():
            freq_set = elem[0]

            if freq_set == frozenset(["60", "104"]):
                print(1)
            for i in range(1, len(freq_set)):
                for subset in combinations(freq_set, i):

                    confidence = frequent_itemset[freq_set] / frequent_itemset[frozenset(subset)]
                    
                    if confidence < self.__min_conf:
                        continue

                    if frozenset(subset) in rules.keys():
                        rules[frozenset(subset)].append([freq_set - frozenset(subset), confidence])
                    else:
                        rules[frozenset(subset)] = [[freq_set - frozenset(subset), confidence]]
                
        return rules






        




        








    


