

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




#---------------------------------------------------------------------#
#------------------------------- Tree --------------------------------#
#---------------------------------------------------------------------#

class IDTree:
    """ Class represent IDTree produces by ID3 and C4.5 algorithm
    
    Class publishes interface to serialize IDTree in a form of Python
    function as well as predicting sample's class

    Attributes
    ----------
    rootNode : IDTreeLeaf or IDTreeNode
        initial roodNode of the tree
    features : list
        list of features present in the tree

    """

    def __init__(self, rootNode=None, features=[]):

        """ Initializes IDTree with a given rootNode

        Parameters
        ----------
        rootNode : IDTreeLeaf or IDTreeNode, optional (default : None)
            initial roodNode of the tree
        features : list, optional (default : [])
            list of features present in the tree
        """
        
        # __rootNode
        if type(rootNode) != IDTreeLeaf and type(rootNode) != IDTreeNode:
            self.__rootNode = None
        else:
            self.__rootNode = rootNode
        # __features
        self.__features = features



        



    ###########################################################################################
    ####################################  Interface  ##########################################
    ###########################################################################################

    def predict(self, sample):
        pass




    def saveAsFunction(self, filename, argName='sample', fileMode='w', indentation=2):

        """ Saves IDTree as a python function

        Parameters
        ----------
        filename : string
            name of the file to write function
        argName : string, optional (default : 'sample')
            name of the argument used in function (argument is a list of fetures)
        fileMode : string, optional (default : 'w')
            mode that will serve to open the file
        indentation : int, optional (default : 2)
            indentation of the formatter  
        """

        # Function header
        functionDefinition = self.__makeHeader()
        # Function body
        functionDefinition = functionDefinition + \
                             self.__makeRuleset(
                                 self.__rootNode, depth=1, argName=argName, indentation= indentation
                             )

        # Write to file
        self.__saveToFile(functionDefinition, filename, fileMode)
        


    # TODO 
    def loadFromFunction(self, filename):
        
        """ Loads IDTree from a function saved by the saveAsFunction() method

        Parameters
        ----------
        filename : string
            name of the file to read function from
        """
        pass




    ###########################################################################################
    ####################################  Utilities  ##########################################
    ###########################################################################################

    def __makeHeader(self):

        """ Creates header to the function made by saveAsFunction() method """

        # Header
        header = "def predict("
        header = header + "sample"
        header = header + "): #"
        
        # Comment to the header
        featuresNumber = len(self.__features)
        for i in range(0, featuresNumber):
            featureName = self.__features[i]
            header = header + "sample[" + str(i) +"]: " + featureName
            if i != featuresNumber - 1:
                header = header + ", "
        header = header + "\n"
        
        return header




    def __makeRuleset(self, node, depth, argName, indentation=2):

        """ Creates if-elif ruleset used by saveAsFunction() method 
        
        Function is designed to create arbitrary if-elif nested structure
        base on the tree given by the 'node' root node.

        Parameters
        ----------
        node : IDTreeNode, IDTreeLeaf
            root node of the tree
        depth : int
            depth of the structure (used to format if-elif structure
            intendation)
        argName : string
            name of the argument of function (list of features' classes)
        indentation : int, optional (default : 2)
            indentation of the formatter             
        """
        #Initialize ruleset
        ruleset = ''

        # If terminal node (leaf)
        if type(node) == IDTreeLeaf:
            targetClass = f"return '{node.getTargetClass()}'"
            ruleset = self.__formatRule(targetClass, depth, indentation)
            return ruleset

        # If intermediate node
        elif type(node) == IDTreeNode:

            keys = list(node.getChildren().keys())
            for key in keys:

                # First child
                if key == keys[0]:
                    rule = f'if {argName}[{node.getFeatureIndex()}]' + key + ':'

                # Inetrmediate or last child
                else:
                    rule = f'elif {argName}[{node.getFeatureIndex()}]' + key + ':' 
                       
                # Format if-elif header
                ruleset = ruleset + self.__formatRule(rule, depth, indentation)
                # Call __makeRuleset() to fullfill if-elif statement (RECURSION)
                ruleset = ruleset + self.__makeRuleset(node.getChildren()[key], depth + 1, argName, indentation)

        # Wrong node's type
        else:
            print(f'__makeRuleset(): Wrong type of the node ({type(node)})')
            raise TypeError()

        # Return ruleset (recursively) 
        return ruleset




    def __formatRule(self, rule, depth, indentation=2):
        """ Formats rule  to write it in the new line of the function 
    
        Parameters
        ----------
        rule : string
            rule to format
        depth : int
            depth of the structure (used to format rule's intendation)
        indentation : int, optional (default : 2)
            indentation of the formatter   
        """
        return ' ' * indentation * depth + rule + '\n'




    def __saveToFile(self, content, filename, fileMode='w'):
        """ Saves content string to the file
        
        Parameters
        ----------
        content : string
            content to write
        filename : string
            name of the file
        fileMode : string, optional (default : 'w')
            mode used to open file
        """
        f = open(filename, fileMode)
        f.write(content)
