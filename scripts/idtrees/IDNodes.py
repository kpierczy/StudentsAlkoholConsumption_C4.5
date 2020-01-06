#---------------------------------------------------------------------#
#------------------------------- Leaf --------------------------------#
#---------------------------------------------------------------------#


class IDTreeLeaf:
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
            
class IDTreeNode:
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