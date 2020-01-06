from idtrees.IDNodes import IDTreeLeaf, IDTreeNode

class ID3Tree:
    """ Class represent IDTree produces by ID3 algorithm
    
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
        """ Returns classification predicted by the IDTree

        Parameters
        ----------
        sample : list
            list of features representing sample
        """
        return self._evaluateNode(self.__rootNode, sample)




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

        # Function footage
        functionDefinition = functionDefinition + "\n" + \
                             ' ' * indentation + \
                             "print('No classification achieved. Check features of the sample')" + "\n" +\
                             ' ' * indentation + \
                             "return False" + "\n"

        # Write to file
        self.__saveToFile(functionDefinition, filename, fileMode)
        



    def loadFromFunction(self, filename):
        
        """ Loads IDTree from a function saved by the saveAsFunction() method

        Parameters
        ----------
        filename : string
            name of the file to read function from
        """

        #---------------------------------------------------#
        #--- TODO** - building tree from python function ---#
        #---------------------------------------------------#

        pass




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
        
        # Intermediate node
        if type(node) == IDTreeNode:
            
            # Iterate over children of the node
            keys = list(node.getChildren().keys())
            for key in keys:
                
                # Nominal feature
                if key.startswith(' == '):
                    # Make comparison
                    if sample[node.getFeatureIndex()] == key[5:len(key) - 1]:
                        # If comparison true, return  actual children's evaluation
                        return self._evaluateNode(node.getChildren()[key], sample)

                #Numerical feature
                elif key.startswith(' <= '):
                    # Make comparison
                    if sample[node.getFeatureIndex()] <= float(key[4:len(key)]):
                        # If comparison true, return  actual children's evaluation
                        return self._evaluateNode(node.getChildren()[key], sample)

                elif key.startswith(' > '):
                    # Make comparison
                    if sample[node.getFeatureIndex()] > float(key[3:len(key)]):
                        # If comparison true, return  actual children's evaluation
                        return self._evaluateNode(node.getChildren()[key], sample)

                # Wrong condition
                else:
                    raise Exception(
                        f"_evaluateNode: wrong children node's condition ({key})"
                    )

            print('_evaluateNode(): impossible to classify sample')
            raise Exception("Check samples arguments")

        # Terminal node (leaf)
        elif type(node) == IDTreeLeaf:
            return node.getTargetClass()





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
