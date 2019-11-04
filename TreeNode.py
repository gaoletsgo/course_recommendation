
# FP Tree Node.

class TreeNode:
    
    def __init__(self, name, parent, count=1):
        """
            @param: name: node name.   
            @param: parent: node parent.   
            @param: count: the number of node name appears.  
        """
        self.__name = name
        self.__parent = parent
        self.__count = count
        self.__children = {}
        self.__next = None
        self.__prev = None

    @property
    def next(self):
        return self.__next
    
    @next.setter
    def next(self, next_node):
        self.__next = next_node
    
    @property
    def prev(self):
        return self.__prev
    
    @prev.setter
    def prev(self, prev_node):
        self.__prev = prev_node
    
    @property
    def name(self):
        """
            node name.
        """
        return self.__name

    @property
    def count(self):
        """
            node count.
        """
        return self.__count
    
    def add_count(self, value=1):
        """
            node count ++.
        """
        self.__count += value
    
    @property
    def children(self):
        """
            node children. dict(key=node_name, value=node)
        """
        return self.__children
    
    @property
    def parent(self):
        """
            node parent.
        """
        return self.__parent

    def __str__(self):
        return "name: "+str(self.__name)+" count: "+str(self.__count)
    