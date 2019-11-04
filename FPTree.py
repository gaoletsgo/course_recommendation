from TreeNode import TreeNode
import numpy as np
from collections import OrderedDict


class FPTree:
    
    def __init__(self, records, min_count):
        self.__root = TreeNode("root", "None")
        self.__data = records
        self.__min_count = min_count
        self.__header_table = {}
       
        for record in records:
            for item_index in record:

                # establish header table.
                if str(item_index) in self.__header_table.keys():
                    self.__header_table[str(item_index)]["count"] += 1
                else:
                    self.__header_table[str(item_index)] = {"count": 1, "nodes": []}
                
               
        # # remove unfrequent item in header table.
        # for item in self.__header_table.copy().items():
        #     if item[1]["count"] < min_count:
        #         self.__header_table.pop(item[0])
        
        # sort table by count in descending.
        self.__header_table = OrderedDict(sorted(self.__header_table.items(), key=lambda item: item[1]["count"], reverse=True))

        # build fp tree.
        for record in records:
            current_node = self.__root

            for item_index in record:

                if str(item_index) in current_node.children.keys():
                    node = current_node.children[str(item_index)]
                    node.add_count()
                    current_node = node
                else:
                    new_child = TreeNode(str(item_index), current_node)
                    current_node.children[str(item_index)] = new_child

                    # add new node to the header table head linkedlist.
                    self.__header_table[str(item_index)]["nodes"].append(new_child)
                    current_node = new_child

    @property
    def header_table(self):
        return self.__header_table

    @header_table.setter
    def header_table(self, key, value):
        self.__header_table[key] = value

    @property
    def root(self):
        return self.__root


    def get_prefix(self, node):
        """
        get node prefix.
        
        Args:
            node (TreeNode): node in fptree.
        
        Returns:
            [0]: prefix_itemlist(list[string]): a list with the prefix item name.   
            [1]: prefix_nodes(list[TreeNode]): a list with prefix node.
        """
        prefix_nodes = []
        prefix_itemlist = []
        current_node = node
        while current_node.parent.name is not "root":
            prefix_nodes.insert(0, current_node.parent)
            prefix_itemlist.insert(0, current_node.parent.name)

            current_node  = current_node.parent

        return prefix_itemlist, prefix_nodes
