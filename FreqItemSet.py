

class FreqItemSet:

    class AssociateRule:

        def __init__(self, if_set, then_set):
            """
                Associate Rule: {if_set} -> {then_set}.
                if_set(np.array): course ind(ex/ices).
                then_set(np.array): course ind(ex/ices).
                dataset (np.array): the associate rule mined from dataset.
            """

            self.__if_set = if_set
            self.__then_set = then_set
            self.__count = 1
            self.__confidence = 0

        @property
        def count(self):
            return self.__count
        
        def add_count(self, value):
            self.__count+=value

        @count.setter 
        def count(self, value):
            self.__count = value

        @property
        def if_set(self):
            return self.__if_set

        @property
        def then_set(self):
            return self.__then_set


        def __hash__(self):
            return hash(str(self.__if_set))+3*hash(str(self.__then_set))


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

    # def get_associate_rules(self, confidence):
    #     rules = set()

    #     if len(self.__item_set) == 1:
    #         AssociateRule()


    def __eq__(self, freq_itemset):
        return self.itemset == freq_itemset.itemset
    
    def __ne__(self, value):
        return not self.__eq__(value)

    def __str__(self):
        return "itemset: "+str(self.__item_set)+" count: "+str(self.__count)

    def __hash__(self):
        return hash(str(self.__item_set))
    