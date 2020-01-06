from idtrees.ID3 import ID3

class C45(ID3):
    """ C4.5 algorithm's implementation base on the extended ID3 algorithm

    As ID3 algorithm's implementations extends some basics concepts of the
    algorithm, including changes introduced by C4.5 (@see ID3), this class
    extendes it only with pruning capability.

    Post pruning is executet on the ID3's result tree to reduce effects of
    overfitting.
    """

    def __init__(self, pruneThreshold, entropyIndicator="gain"):
    
        """ Initializes C4.5 algorithm
        
        Parameters
        ----------
        pruneThreshold : float
            value of threshold used during identification tree's post-pruning
        entropyIndicator : ['gain', 'gainRatio', 'gini'], optional (default : 'gain')
            method of measuring entropy/impurity of computed feature/target classes
        """

        super().__init__(entropyIndicator)
        self.__pruneThreshold = pruneThreshold




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
        tree : IDTree
            result identification tree
        """

        tree = super().compute(df)

        #--------------------------------#
        #--- TODO - implement pruning ---#
        #--------------------------------#