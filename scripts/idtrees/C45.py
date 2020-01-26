from idtrees.ID3 import ID3
from idtrees.C45Tree import C45Tree

class C45(ID3):
    """ C4.5 algorithm's implementation base on the extended ID3 algorithm

    As ID3 algorithm's implementations extends some basics concepts of the
    algorithm, including changes introduced by C4.5 (@see ID3), this class
    extendes it only with pruning capability.

    Post pruning is executet on the ID3's result tree to reduce effects of
    overfitting.
    """

    def __init__(self, entropyIndicator="gain"):
    
        """ Initializes C4.5 algorithm """

        super().__init__(entropyIndicator)



    ###########################################################################################
    ####################################  Algorithm  ##########################################
    ###########################################################################################

    def compute(self, df):
        """ Computes IDTreee with C4.5 algorithm
        
        Extends ID3.compute() with post-pruning mechanism
        
        Parameters
        ----------
        df : pandas.DataFrame
            set of traning data
        
        Returns
        -------
        tree : C45Tree
            result identification tree
        """

        return C45Tree(super().compute(df.copy()), df)