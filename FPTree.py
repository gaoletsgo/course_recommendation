import numpy as np  


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
            return self.__children
        
        def get_all_children_name(self):
            return [child.get_node_name() for child in self.__children]

        def search_child(self, name):
            for child in self.__children:
                if child.get_node_name() == name:
                    return child
                else: 
                    return None

        def get_node_name(self):
            return self.__node_name
        
        def get_count(self):
            return self.__count
        
        def __str__(self):
            return str(self.__node_name)+": "+str(self.__count)

    def __init__(self):
        self.__root = self.Node()
    
    def get_root(self):
        return self.__root
    
  
    