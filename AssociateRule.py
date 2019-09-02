

class AssociateRule:


    def __init__(self, if_set, then_set, dataset):
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
        self.__dataset = dataset

    @property
    def count(self):
        return self.__count
    
    def add_count(self, value):
        self.__count+=value

    @count.setter 
    def count(self, value):
        self.__count = value

    @property
    def confidence(self):



        return self.__count/


    
