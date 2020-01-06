from idtrees.ID3Tree import ID3Tree
from idtrees.IDNodes import IDTreeLeaf, IDTreeNode

class C45Tree(ID3Tree):
    """ Class represent IDTree produces by C4.5 algorithm
    
    Class extends ID3Tree (@see ID3Tree) with possibility to
    calculate classifications' probability of a sample with
    missing features. 

    Attributes
    ----------
    rootNode : IDTreeLeaf or IDTreeNode
        initial roodNode of the tree
    features : list
        list of features present in the tree

    """
    
    def __init__(self, rootNode=None, features=[]):

        """ Initializes C45Tree with a given rootNode

        Parameters
        ----------
        rootNode : IDTreeLeaf or IDTreeNode, optional (default : None)
            initial roodNode of the tree
        features : list, optional (default : [])
            list of features present in the tree
        """
        
        super().__init__(rootNode, features)




    ###########################################################################################
    ####################################  Utilities  ##########################################
    ###########################################################################################

    def _evaluateNode(self, node, sample):
        """ Evaluates tree that has root in the 'node'

        Parameters
        ----------
        node : IDTreeNode, IDTreeLeaf
            node representing tree to evaluate
        sample : list
            list of features to evaluate tree with respect to

        Returns
        -------
        classification : string
            clasification of the sample
        """

        #-----------------------------------------------------------------------------#
        #---- TODO* - implement evaluation with incomplete samples classification ----#
        #-----------------------------------------------------------------------------#