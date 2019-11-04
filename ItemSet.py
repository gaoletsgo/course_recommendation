

class ItemSet:

    def __init__(self, itemset, support):
        """
        init Itemset.
        
        Args:
            itemset (frosenset): A forsenset contains different items.  
            support (Float): Itemset support. 
        """
        self.__itemset = itemset
        self.__support = support
    
    @property
    def support(self):
        return self.__support

    @support.setter
    def support(self, value):
        self.__support = value
    
    @property
    def itemset(self):
        return self.__itemset
    
    def __eq__(self, itemset_obj):
        return self.__itemset == itemset_obj.itemset

    def __ne__(self, itemset_obj):
        return not self.__eq__(itemset_obj)

    def __str__(self):
        return str(set(self.__itemset))+" sup: "+str(self.__support)

    # def __hash__(self):
    #     """
    #     ItemSets that  have same itemset value should have same hash value. 
        
    #     Returns:
    #         Int: Hash value of the ItemSet.itemset.
    #     """
    #     hash_value = 0
    #     for e in self.__itemset:
    #         hash_value += hash(str(e))
    #     return hash_value

