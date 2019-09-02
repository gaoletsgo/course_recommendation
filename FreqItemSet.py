

class FreqItemSet:

    def __init__(self, item_set, count):
        """
            itemset(Set): set of string course indices. 
        """
        self.__item_set = item_set
        self.__count = count


    @property
    def itemset(self):
        return self.__item_set
    
    @itemset.setter
    def itemset(self, value):
        """
        input: 
            value(Set): the set that would insert into the itemset.
        """
        self.__item_set = self.__item_set | value

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value

    def __eq__(self, freq_itemset):
        return self.itemset == freq_itemset.itemset
    
    def __ne__(self, value):
        return not self.__eq__(value)

    def __str__(self):
        return "itemset: "+str(self.__item_set)+" count: "+str(self.__count)

    def __hash__(self):
        return hash(str(self.__item_set))
    