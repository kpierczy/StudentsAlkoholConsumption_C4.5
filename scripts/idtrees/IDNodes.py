import operator

#---------------------------------------------------------------------#
#----------------------------- Base node -----------------------------#
#---------------------------------------------------------------------#

class IDTreeBaseNode:
    """ Class represents generic node of the ID Tree (intermediate node or leaf)
    
    Class implements common attributes and methods for both leaves and
    intermediate nodes.
    """

    def __init__(self):
        
        """ Initializes IDTreeLeaf with a name of a target class

        Parameters
        ----------
        targetClass : string
            name of the targetClass to be pointed by the Leaf
        
        Attributes
        ----------
        __description : object
            additional description of the node. An arbitrary class' instance
            can be used.
        """

        self._parentNode = None
        self.__description = None

    def getParentNode(self):

        """ Returns parent node """
        return self._parentNode

    def setParentNode(self, parentNode):

        """ Set new class pointed by the leaf
        
        Parameters
        ----------
        parentNode : object
            new parent node

        Returns
        -------
        False : bool
            parent node is of a wrong type
        True : bool
            parent node set
        """

        if type(parentNode) == IDTreeNode:
            self._parentNode = parentNode
            return True
        else:
            return False

    def getDescription(self):

        """ Returns node's description """
        return self.__description

    def setDescription(self, description):

        """ Set description for the node
        
        Parameters
        ----------
        description : object
            new description
        """

        self.__description = description
    



#---------------------------------------------------------------------#
#------------------------------- Leaf --------------------------------#
#---------------------------------------------------------------------#


class IDTreeLeaf(IDTreeBaseNode):
    """ Class represents leaf of the IDTree
    
    Leaves of and id tree represent target classes choosen
    by the tree for particular samples.
    """

    def __init__(self, targetClass):
        
        """ Initializes IDTreeLeaf with a name of a target class

        Parameters
        ----------
        targetClass : string
            name of the targetClass to be pointed by the Leaf
        """
        self.__targetClass = targetClass

    def getTargetClass(self):

        """ Returns class pointed by the leaf """
        return self.__targetClass

    def setTargetClass(self, targetClass):

        """ Set new class pointed by the leaf
        
        Parameters
        ----------
        targetClass : string
            new target class

        Returns
        -------
        False : bool
            target Class is not a string
        True : bool
            new target class set
        """

        if type(targetClass) is str:
            self.__targetClass = targetClass
            return True
        else:
            return False
            
            


#---------------------------------------------------------------------#
#------------------------------- Node --------------------------------#
#---------------------------------------------------------------------#
            
class IDTreeNode(IDTreeBaseNode):
    """ Class represents intermediate node of the identification tree 
    
    Children of the node are represented byt dictionary pairs
    {'string' : object} where string is formula leading to a particular
    child and object is a child

    --- Important ---

    string representing formula HAVE TO be in one of two form:
    1) for numerical feature : " <= featureValue" or " > featureValue"
    2) for nominal feature : " == 'featureClass'"

    """

    def __init__(self, featureIndex):
        
        """ Initializes IDTree Node with an index of a feature 
        
        Attribute is a feature that is checked by this node. Initial
        children dictionary is empty

        Parameters
        ----------
        featureIndex : int
            index of a feature (column) in the features set (it's used while
            serializing tree into python function)
        """

        self.__featureIndex = featureIndex
        self.__children = {}

    def getFeatureIndex(self):    
        """ Returns feature's index """
        return self.__featureIndex

    def setFeatureIndex(self, featureIndex):
        """ Set new feature index
        
        Parameters
        ----------
        featureIndex : int
            new feature's index
        Returns
        -------
        False : bool
            featureIndex is not a non-negative int
        True : bool
            new featureIndex set
        """

        if type(featureIndex) is int and featureIndex >= 0:
            self.__featureIndex = featureIndex
            return True
        else:
            return False

    def getChildren(self):
        """ Returns children of the node """
        return self.__children

    def addChild(self, childFormula, child):

        """ Adds new child for the node

        --- Important ---

        Method does NOT validate logical consistency of the children
        set (i.e. it is able to add ' <= 8' child when there is
        ' <= 12')
        
        Parameters
        ----------
        childFormula : string
            new child's formula (should be in form given in class description)
        child : IDTreeNode, IDTreeLeaf
            new child

        Returns
        -------
        False : bool
            childFormula is of a bad format or child is of a wrong type
        True : bool
            new child added
        """

        if len(childFormula) <= 3 or \
           (len(childFormula) == 4 and childFormula[0:3] != ' > '):
            print('addChild(): child formula is too short (', childFormula, ')')
            return False
        elif (not (childFormula[0:4] in [' == ', ' <= '])) and \
             (not childFormula[0:3] == ' > '):
            print(f'addChild(): child formula is of a wrong format ({childFormula})')
            return False
        elif type(child) != IDTreeLeaf and type(child) != IDTreeNode:
            print('addChild(): child type should be IDTreeLeaf or IDTreeNode (actual: ', type(child), ')')
        else:
            self.__children[childFormula] = child
            self.__children[childFormula].setParentNode(self)
            return True

    def removeChild(self, childFormula):

        """ Child child for the node
        
        Parameters
        ----------
        childFormula : string
            child's formula to remove

        Returns
        -------
        False : bool
            no childFormula in chldren set
        True : bool
            child removed
        """

        if not (childFormula in list(self.__children.keys())):
            print('removeChild(): no such formula in children set')
            return False
        else:
            self.__children.pop(childFormula, None)
            return True



#---------------------------------------------------------------------#
#------------------------ Node's statistics --------------------------#
#---------------------------------------------------------------------#

class NodeStatistics:
    """ Node's statistics used by the C4.5 algorithm during gathering 
        nodes' statistics for the prunning procedure

    Attributes
    ----------
    evaluatedSamples : int
        number of samples from the training set that was evaluated by the
        node
    wrongClassified : int
        number of samples from the training set that was incorectly classified
    wrongClassified : int
        number of samples from the training set that would be incorectly classified
        if the node would be a leaf with a target class set to the most popular
        class returned by this node within the training data set
    classifications : dictionary {'string' : int}
        statistics of the samples' classifications. Key is a class that was
        indicated by the node and value is number of samples that was
        classified as belonging to this class.
    """
    
    def __init__(self):
        """ Initializes empty statistics """
        self.__evaluatedSamples = 0
        self.__conditionallyEvaluatedSamples = 0
        self.__wrongClassified = 0
        self.__conditionallyWrongClassified = 0
        self.__classifications = dict()

    def getEvaluatedSamples(self):
        """ Return's number of samples evaluated by the node """
        return self.__evaluatedSamples

    def setEvaluatedSamples(self, evaluatedSamples):
        """ Set new number of evaluated samples
        
        Parameters
        ----------
        evaluatedSamples : int
            new number of evaluated samples
        Returns
        -------
        False : bool
            evaluatedSamples is not a non-negative int
        True : bool
            new evaluatedSamples set
        """

        if type(evaluatedSamples) is int and evaluatedSamples >= 0:
            self.__evaluatedSamples = evaluatedSamples
            return True
        else:
            return False

    def getConditionallyEvaluatedSamples(self):
        """ Return's number of samples that would be evaluated by the node if it classify samples
            with the most popular class returned by this node on the training set.
        """
        return self.__conditionallyEvaluatedSamples

    def setConditionallyEvaluatedSamples(self, conditionallyEvaluatedSamples):
        """ Set new number of samples that would be evaluated by the node if it classify samples
            with the most popular class returned by this node on the training set.
        
        Parameters
        ----------
        conditionallyEvaluatedSamples : int
            new number of evaluated samples
        Returns
        -------
        False : bool
            evaluatedSamples is not a non-negative int
        True : bool
            new evaluatedSamples set
        """

        if type(conditionallyEvaluatedSamples) is int and conditionallyEvaluatedSamples >= 0:
            self.__conditionallyEvaluatedSamples = conditionallyEvaluatedSamples
            return True
        else:
            return False

    def getWrongClassified(self):
        """ Return's number of from the training data set that were wrong classified by the node """
        return self.__wrongClassified

    def setWrongClassified(self, wrongClassified):
        """ Set new number of from the training data set that were wrong classified by the node
        
        Parameters
        ----------
        wrongClassified : int
            new number of wrong classified samples
        Returns
        -------
        False : bool
            wrongClassified is not a non-negative int
        True : bool
            new wrongClassified set
        """

        if type(wrongClassified) is int and wrongClassified >= 0:
            self.__wrongClassified = wrongClassified
            return True
        else:
            return False

    def getConditionallyWrongClassified(self):
        """ Return's number of from the training data set that would be wrong classified by the node
            if it would classify samples with the most popular class returned on the training set.
        """
        return self.__conditionallyWrongClassified

    def setConditionallyWrongClassified(self, conditionallyWrongClassified):
        """ Set new number of from the training data set that would be wrong classified by the node
            if it would classify samples with the most popular class returned on the training set.
        
        Parameters
        ----------
        conditionallyWrongClassified : int
            new number of samples that would be incorrectly classified
            if the node would be a leaf with a target class set to the most popular
            class returned by this node within the training data set
        Returns
        -------
        False : bool
            wrongClassified is not a non-negative int
        True : bool
            new wrongClassified set
        """

        if type(conditionallyWrongClassified) is int and conditionallyWrongClassified >= 0:
            self.__conditionallyWrongClassified = conditionallyWrongClassified
            return True
        else:
            return False

    def addClassification(self, classification):
        """ Adds new classification to the __classifications dictionary

        If a classification is already in the dictionary, it's counter
        is incremented

        Parameters
        ----------
        classification : string
            classification to add to the dictionary
        Returns
        -------
        False : bool
            classification is not a string
        True : bool
            new classification add
        """

        if not isinstance(classification, str):
            return False
        else:
            if classification in self.__classifications.keys():
                self.__classifications[classification] = \
                    self.__classifications[classification] + 1
            else:
                self.__classifications[classification] = 1

    def getMostPopularClassification(self):
        """ Returns the most often classification returned by the node 
        
        Returns
        -------
        classification : string
        """

        return max(self.__classifications.items(), key=operator.itemgetter(1))[0]