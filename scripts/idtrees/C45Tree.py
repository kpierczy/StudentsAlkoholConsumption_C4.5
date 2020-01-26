from math import sqrt
from idtrees.IDTree import IDTree
from idtrees.IDNodes import IDTreeLeaf, IDTreeNode, NodeStatistics

class C45Tree(IDTree):
    """ Class represent IDTree produces by C4.5 algorithm
    
    Class extends IDTree (@see IDTree) with possibility to
    calculate classifications' probability of a sample with
    missing features. 

    Attributes
    ----------
    rootNode : IDTreeLeaf or IDTreeNode
        initial roodNode of the tree
    features : list
        list of features present in the tree

    """
    
    def __init__(self, idTree, df):

        """ Initializes C45Tree with a given rootNode

        Parameters
        ----------
        idTree : IDTree
            tree to be wrapped by the C45Tree (idTree remains empty after warapping)
        df : pandas.DataFrame
            set of traning data used to prune
        """ 
    
        super().__init__(idTree._rootNode, idTree._features)
        idTree._rootNode = None
        idTree._features = None

        self.__prune(df)



    ###########################################################################################
    ####################################  Utilities  ##########################################
    ###########################################################################################

    def __prune(self, df):
        """ Prunes tree with a given training set

        Parameters
        ----------
        df : pandas.DataFrame
            set of traning data used to prune
        """
    
        # Initialize nodes' statistics
        self.__initializeStatistics(self._rootNode)

        # Compute statistics used for prunning
        for i in range(df.shape[0]):
            sample = df.iloc[i].tolist()
            self.__updateStatistics(self._rootNode, sample)

        # Compute conditional statistics used for prunning
        for i in range(df.shape[0]):
            sample = df.iloc[i].tolist()
            self.__updateConditionalStatistics(self._rootNode, sample)

        # Perform prunning
        self.__prunningEvaluation(self._rootNode, "")

        # Clear Statistics
        self.__clearStatistics(self._rootNode)



    def __initializeStatistics(self, node):
        """ Initializes all intermediate nodes' description with NodeStatistics object 
        
        Parameters
        ----------
        node : IDTreeNode, IDTreeLeaf
            node representing tree to evaluate
        """

        # Intermediate node
        if type(node) == IDTreeNode:

            # Initialize node's statistics if not initialized yet
            node.setDescription(NodeStatistics())

            # Iterate over children of the node
            keys = list(node.getChildren().keys())
            for key in keys:
                self.__initializeStatistics(node.getChildren()[key])



    def __clearStatistics(self, node):
        """ Clears all intermediate nodes' description with NodeStatistics object 
        
        Parameters
        ----------
        node : IDTreeNode, IDTreeLeaf
            node representing tree to evaluate
        """

        # Intermediate node
        if type(node) == IDTreeNode:

            # Initialize node's statistics if not initialized yet
            node.setDescription(None)
            
            # Iterate over children of the node
            keys = list(node.getChildren().keys())
            for key in keys:
                self.__initializeStatistics(node.getChildren()[key])



    def __updateStatistics(self, node, sample):
        """ Update ID Tree's intermediate nodes's statistics base on the sample

        Parameters
        ----------
        node : IDTreeNode, IDTreeLeaf
            node representing tree to evaluate
        sample : list
            list represnting a sample from the training set
        """

        # Intermediate node
        if type(node) == IDTreeNode:
            
            # Iterate over children of the node
            keys = list(node.getChildren().keys())
            for key in keys:
                
                # Nominal feature
                if key.startswith(' == '):
                    # Make comparison
                    if sample[node.getFeatureIndex()] == key[5:len(key) - 1]:
                        # If comparison true, get  actual children's evaluation
                        classification =  self.__updateStatistics(node.getChildren()[key], sample)
                        # Update node's staictics
                        self.__updateNodeStatistics(node, classification, sample[len(sample) - 1])
                        return classification

                #Numerical feature
                elif key.startswith(' <= '):
                    # Make comparison
                    if sample[node.getFeatureIndex()] <= float(key[4:len(key)]):
                        # If comparison true, get  actual children's evaluation
                        classification =  self.__updateStatistics(node.getChildren()[key], sample)
                        # Update node's staictics
                        self.__updateNodeStatistics(node, classification, sample[len(sample) - 1])
                        return classification

                elif key.startswith(' > '):
                    # Make comparison
                    if sample[node.getFeatureIndex()] > float(key[3:len(key)]):
                        # If comparison true, get  actual children's evaluation
                        classification =  self.__updateStatistics(node.getChildren()[key], sample)
                        # Update node's staictics
                        self.__updateNodeStatistics(node, classification, sample[len(sample) - 1])
                        return classification

                # Wrong condition
                else:
                    raise Exception(
                        f"__evaluateNode: wrong children node's condition ({key})"
                    )

            print('__evaluateNode(): impossible to classify sample')
            raise Exception("Check samples arguments")

        # Terminal node (leaf)
        elif type(node) == IDTreeLeaf:
            return node.getTargetClass() 



    def __updateConditionalStatistics(self, node, sample):
        """ Updates conditional ID Tree's intermediate nodes's statistics base on the sample

        Parameters
        ----------
        node : IDTreeNode, IDTreeLeaf
            node representing tree to evaluate
        sample : list
            list represnting a sample from the training set
        """

        # Intermediate node
        if type(node) == IDTreeNode:
            
            # Iterate over children of the node
            keys = list(node.getChildren().keys())
            for key in keys:
                
                # Nominal feature
                if key.startswith(' == '):
                    # Make comparison
                    if sample[node.getFeatureIndex()] == key[5:len(key) - 1]:
                        # Reccursive call
                        self.__updateConditionalStatistics(node.getChildren()[key], sample)
                        # Update node's staictics
                        self.__updateNodeConditionalStatistics(node, sample[len(sample) - 1])
                        return

                #Numerical feature
                elif key.startswith(' <= '):
                    # Make comparison
                    if sample[node.getFeatureIndex()] <= float(key[4:len(key)]):
                        # Reccursive call
                        self.__updateConditionalStatistics(node.getChildren()[key], sample)
                        # Update node's staictics
                        self.__updateNodeConditionalStatistics(node, sample[len(sample) - 1])
                        return

                elif key.startswith(' > '):
                    # Make comparison
                    if sample[node.getFeatureIndex()] > float(key[3:len(key)]):
                        # Reccursive call
                        self.__updateConditionalStatistics(node.getChildren()[key], sample)
                        # Update node's staictics
                        self.__updateNodeConditionalStatistics(node, sample[len(sample) - 1])
                        return

                # Wrong condition
                else:
                    raise Exception(
                        f"__evaluateNode: wrong children node's condition ({key})"
                    )

            print('__evaluateNode(): impossible to classify sample')
            raise Exception("Check samples arguments")



    def __updateNodeStatistics(self, node, classification, realClassification):
        """ Updates node's statictics basing on the classification value 
        
        Parameters
        ----------
        node : IDTreeNode, IDTreeLeaf
            node to be updated
        classification : string
            classification returned by the node
        realClassification : string
            evaluated sample from the training data set used to update statictics
        """

        # Number of samples evaluated by the node
        node.getDescription().setEvaluatedSamples(
            node.getDescription().getEvaluatedSamples() + 1
        )

        # Classifications dictionary
        node.getDescription().addClassification(classification)

        # Wrong classified
        if(classification != realClassification):
            node.getDescription().setWrongClassified(
                node.getDescription().getWrongClassified() + 1
            )



    def __updateNodeConditionalStatistics(self, node, realClassification):
        """ Updates node's conditional statictics 
        
        Parameters
        ----------
        node : IDTreeNode, IDTreeLeaf
            node to be updated
        realClassification : string
            evaluated sample from the training data set used to update statictics
        """
        
        # Number of samples conditionally evaluated by the node
        node.getDescription().setConditionallyEvaluatedSamples(
            node.getDescription().getConditionallyEvaluatedSamples() + 1
        )

        # Update conditional wrong classification
        if node.getDescription().getMostPopularClassification() != realClassification:
            node.getDescription().setConditionallyWrongClassified(
                node.getDescription().getConditionallyWrongClassified() + 1
            )



    def __prunningEvaluation(self, node, nodesFeature):
        """ Performs prunning of the tree given with a root node.
        Prunning process is based on the nodes' descriptions which are
        supposed to be NodeStatictics objects.

        Paramaters
        ----------
        node : IDTreeNode, IDTreeLeaf
            root node of the tree to be pruned 
        nodesFeature : string
            feature of the node that is assigned to it in the parent node
        """

        # Intermediate node
        if type(node) == IDTreeNode:
            
            # Iterate over children of the node
            keys = list(node.getChildren().keys())
            for key in keys:
                
                # Prune children
                self.__prunningEvaluation(node.getChildren()[key], key)

                # If doesn not evaluate root node
                if nodesFeature != "":

                    if self.__prunePredicate(node):
                        # Replace the node with a leaf
                        node.getParentNode().getChildren()[nodesFeature] = \
                            IDTreeLeaf(node.getDescription().getMostPopularClassification())



    def __prunePredicate(self, node):
        """ Returns true if node should be pruned and false otherwise """

        # Prune the node
        estimatedTestError = self.__estimateTestError(
            node.getDescription().getWrongClassified(), \
            node.getDescription().getEvaluatedSamples()
        )

        estimatedConditionalTestError = self.__estimateTestError(
            node.getDescription().getConditionallyWrongClassified(), \
            node.getDescription().getEvaluatedSamples()
        )

        if estimatedTestError >= estimatedConditionalTestError:
            return True
        else:
            return False



    def __estimateTestError(self, wrongClassified, evaluatedSampels):
        """ Esitmates training set error basing on the training set error
        
        Parameters
        ----------
        wrongClassified : int
            number of samples that were incorrectly classified by the node
        evaluatedSamples : int
            number of samples evaluated by the node
        
        Returns
        -------
        esitmatedTestError : float
        """

        trainingError = wrongClassified / evaluatedSampels
        return trainingError + sqrt(trainingError * (1 - trainingError)) / evaluatedSampels