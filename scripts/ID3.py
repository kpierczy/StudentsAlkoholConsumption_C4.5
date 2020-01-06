import math
import numpy as np
from IDTree import IDTree, IDTreeNode, IDTreeLeaf

class ID3:

    """ Implementation of ID3 classifier algorithm 
    
    Implementation of algorithm slightly extends possibilities of a classical
    approach by adding:
        - additional ways to measure entropy/impurity (not only information
          gain but also gain ratio and gini index)
        - converting numerical features to two separate nominal classes
          (<=x and >x) with the optimal border (x) computation (idea
          from C4.5 algorithm)

    Simple interface make it able to configure entropy measurement method
    and compute result tree in two lines of code, so it is easy to make
    comparison between different training data sets with the least code amount
    possible.

    --- IMPORTANT ---

    Alle methods od the class that operates on data assumes that the data are
    encapsulated in pandas.DataFrame and have a special format:

    Feature_1 Feature_2 Feature_3 --------- Feature_N Target
        -         -         -                   -        -  
        -         -         -                   -        -  
        -         -         -                   -        -  
        -         -         -                   -        -  

    where 'Feature_x' is the name of the feature and 'Target' is fixed header
    used for decision classes

    """
    
    def __init__(self, entropyIndicator="gain"):

        """ Initializes algorithm with choosen entropy measurement method 
        
        Parameters
        ---------
        entropyIndicator : ['gain', 'gainRatio', 'gini'], optional (default : 'gain')
            method of measuring entropy/impurity of computed
            feature/target classes
        """
        if entropyIndicator in ['gain', 'gainRatio', 'gini']:
            self.__entropyIndicator = entropyIndicator
        else:
            self.__entropyIndicator = 'gain'




    ###########################################################################################
    #############################  Configuration interface  ###################################
    ###########################################################################################

    def getEntropyIndicator(self):
        """ Returns actual entropyIndicator"""
        return self.__entropyIndicator

    def setEntropyIndicator(self, entropyIndicator):
        """ Sets a new value for entropyIndicator 
        
        Parameters
        ----------
        entropyIndicator : ['gain', 'gainRatio', 'gini']
            method of measuring entropy/impurity of computed
            feature/target classes
        
        Returns
        -------
        False : bool
            wrong entropyIndicator given
        True : bool
            new entropyIndicator set
        """
        
        if entropyIndicator in ['gain', 'gainRatio', 'gini']:
            self.__entropyIndicator = entropyIndicator
            return True
        else:
            return False




    ###########################################################################################
    ####################################  Algorithm  ##########################################
    ###########################################################################################

    def compute(self, df):
        """ Computes IDTreee with ID3 algorithm
        
        This method is distinguished from self.__buildTree() for two reasons:
            - latter interface consistency with derived classes
            - possible introduction of statostics utilities that would
              measure accuracy of the built tree
        
        Parameters
        ----------
        df : pandas.DataFrame
            set of traning data
        
        Returns
        -------
        tree : IDTree
            result identification tree
        """

        # Check if valid data forat
        columnLabels = df.columns.tolist() 
        targetLabel = columnLabels[len(columnLabels) - 1]
        if targetLabel != 'Target':
            print("Expected: Target, Actual: ",targetLabel)
            raise ValueError("Please validate data's form before calling algorithm")

        # Initialize dictionary containing features types (numerical or nominal)
        featuresTypes = dict() 
        featuresNumber = df.shape[1]-1
        for i in range(0, featuresNumber):
            featureName = df.columns[i]
            featuresTypes[featureName] = df[featureName].dtypes

        return IDTree(self.__buildTree(df, featuresTypes), list(featuresTypes.keys()))




    @staticmethod
    def prepareData(df, targetName, features=None):
        """ Prepares df.DataFrame with arbitrary numer of columns to be used with ID3 class

        Required dataset format:

        Feature_1 Feature_2 Feature_3 --------- Feature_N_1 Feature_N
            -         -         -                    -          -  
            -         -         -                    -          -  
            -         -         -                    -          -  
            -         -         -                    -          -  

        Parameters
        ---------
        df : pandas.DataFrame
            data set to prepare
        targetName : string
            name of the column to be set as a target
        features : list of strings, optional (default : all features)
            names of columns to be selected as features

        Returns
        -------
        newDf : pandas.DataFrame
            formated data set
        """

        # Check if target present
        if not (targetName in df.columns.tolist()):
            print('prepareData(): No such target in data set')
            return

        # All columns used in the data set
        if features is None:
            columnsNames = df.columns.tolist()
            # Remove target feature's name from the columns list
            columnsNames.remove(targetName)
            # Insert traget column to the end position
            newDf = df[columnsNames + [targetName]]
        # Target present in features list
        elif targetName in features:
            print('prepareData(): Target cannot be present in features list')
            return
        # Part of columns used in the data set
        elif all(name in df.columns.tolist() for name in features):
            # Insert traget column to the end position
            newDf = df[features + [targetName]]
        # Absent columns names given
        else:
            print('prepareData(): features list containt lacking names of columns')
            for name in features:
                if not (name in df.columns.tolist()):
                    print('- ', name)
            return

        newDF = newDf.rename(columns={targetName : 'Target'})

        return newDF




    ###########################################################################################
    ####################################  Utilities  ##########################################
    ###########################################################################################

    def __calculateEntropy(self, df):
        """ Calculates entropy of given data set with respect to Target's classes 
        
        Parameters
        ---------
        df : pandas.DataFrame
            data set to compute entropy for
        
        Returns
        -------
        entropy : double
            values of entropy/impurity for a givent data set

        """
        
        # Get number of samples and number of classes in the target
        samples = df.shape[0]
        targetClasses = df['Target'].value_counts().keys().tolist()
        entropy = 0

        # Calculate and sum elements of entropy for every class
        for i in range(0, len(targetClasses)):
            num_of_decisions = df['Target'].value_counts().tolist()[i]		
            classProbability = num_of_decisions/samples
            entropy = entropy - classProbability*math.log(classProbability, 2)
            
        return entropy




    def __chooseFeature(self, df):
        """ Chooses the best feature to get as the next tree's node
        
        Parameters
        ---------
        df : pandas.DataFrame
            data set to analyse features for.
            TAKE CARE: df is muted during computation so pass
            copy of original data to avoid it's loss
        
        Returns
        -------
        bestFeatureName : string
            name of the best feature to get

        """

        #--------------------------------------------#
        #-- Find entropy/impurity of the whole set --#
        #--------------------------------------------#
        
        entropy = self.__calculateEntropy(df)

        featuresNumber = df.shape[1] - 1
        samplesNumber = df.shape[0]

        gains = []
        gainratios = []
        ginis = []

        #------------------------------------------#
        #-------- Look for the best feature -------#
        #------------------------------------------#

        # For each feature
        for i in range(0, featuresNumber):

            featureName = df.columns[i]
            featureType = df[featureName].dtypes
            
            # Translate numeric data from 'featureName' feature to nominal classes
            if featureType != 'object':
                df = self.__convertToNominal(df, featureName, entropy)            

            # List of classes in actually anylised fature
            classes = df[featureName].value_counts()
            
            # Initial values for possible indicators
            gain = entropy
            splitinfo = 0
            gini = 0
            
            #--------------(for loop)------------------#
            #-- Find entropies/impurities of subsets --#
            #------------------------------------------#
            for j in range(0, len(classes)):

                # Get current class name
                currentClass = classes.keys().tolist()[j]
                # Get rows (samples) where feature is equal to 'currentClass'
                subdataset = df[df[featureName] == currentClass]
                # Count number of samples in 'currentClass'
                subsetSamplesNumber = subdataset.shape[0]
                # Calculate ratio of the samples present in 'currentClass'
                classProbability = subsetSamplesNumber/samplesNumber
                
                # Calculate normalized information gain
                subsetEntropy = self.__calculateEntropy(subdataset)
                gain = gain - classProbability * subsetEntropy			
                
                # Calculate normalized splinfo if gainRatio indicator choosen
                if self.__entropyIndicator == 'gainRatio':
                    splitinfo = splitinfo - classProbability*math.log(classProbability, 2)
                # Calculate gini index if gini indicator choosen
                elif self.__entropyIndicator == 'gini':
                    targetClasses = subdataset['Target'].value_counts().tolist()
                    subgini = 1
                    for k in range(0, len(targetClasses)):
                        subgini = subgini - math.pow((targetClasses[k]/subsetSamplesNumber), 2)
                    gini = gini + (subsetSamplesNumber / samplesNumber) * subgini

            #----------------(for loop ends)-----------------#
            #---- Save entropy/imputiry for every feature----#
            #------------------------------------------------#

            #----- Information Gain -----#  
            if self.__entropyIndicator == 'gain':
                gains.append(gain)

            #-- Information Gain Ratio --#
            elif self.__entropyIndicator == 'gainRatio':
                # If e.g. data set consists of 2 rows and current
                # feature consists of 1 class splitinfo can be equal
                # to 0 which prevents algorithm from making x/splitinfo
                # division
                # 
                # In this case decision still can be made. If we set 
                # splitinfo to a large value to make gain ratio very
                # small. This way, we won't find this column as the
                # most dominant one.
                if splitinfo == 0:
                    splitinfo = 100 
                gainratio = gain / splitinfo
                gainratios.append(gainratio)
            
            #-------- Gini Index --------#
            elif self.__entropyIndicator == 'gini':
                ginis.append(gini)
        
        #------------------------------------------#
        #----- Return name of the best feature ----#
        #------------------------------------------#
        
        if self.__entropyIndicator == 'gain':
            bestFeatureIndex = gains.index(max(gains))
        elif self.__entropyIndicator == 'gainRatio':
            bestFeatureIndex = gainratios.index(max(gainratios))
        elif self.__entropyIndicator == 'gini':
            bestFeatureIndex = ginis.index(min(ginis))

        bestFeatureName = df.columns[bestFeatureIndex]
        return bestFeatureName




    def __buildTree(self, df, featuresTypes):
        """ Build IDTree recursively
        
        Parameters
        ----------
        df : pandas.DataFrame
            data set to produces tree with

        Returns
        -------
        tree : IDTree
            tree build with an algorithm
        featuresTypes : dictionary {'featureName' : type}
            dictionary containing pairt name-type for the 
            features in analysed data set
        """

        #------------------------------------------#
        #-------- Prepare for building tree -------#
        #------------------------------------------#

        df_copy = df.copy()
        bestFeature = self.__chooseFeature(df)
        
        # Restore all numerical collumns in df except 'bestFeature'
        # (they were modified in __chooseFeature() by __convertToNominal()
        # during looking for the bestFeature)
        #
        # We want to leave non-choosen numerical features at they were
        # because in the next layers of the tree algorithm can choose
        # different threshold for them
        columns = df.shape[1]
        for i in range(0, columns-1):
            featureName = df.columns[i]
            column_type = featuresTypes[featureName]
            if column_type != 'object' and featureName != bestFeature:
                df[featureName] = df_copy[featureName]

        # Check if feature is numerical
        numericColumn = False
        if featuresTypes[bestFeature] != 'object':
            numericColumn = True

        # Find winner index (number of column in df)
        j = 0 
        for i in featuresTypes:
            if i == bestFeature:
                bestFeatureIndex = j
            j = j + 1



        # Count classes present in df in the 'bestFeature' feature
        classes = df[bestFeature].value_counts().keys().tolist()

        # Initialize node to be return by the method's call
        returnNode = IDTreeNode(bestFeatureIndex)

        #---------------(for loop)-----------------#
        #--------- Recursively build tree ---------#
        #------------------------------------------#

        for i in range(0,len(classes)):
            # Check currently unfolded class of 'bestFeature' feature
            currentClass = classes[i]
            # Take only rows, where 'bestFeature' feature is equal to 'currentClass'
            subdataset = df[df[bestFeature] == currentClass]
            # Drop 'bestFeature' column from the 'subdataset'
            # (It contains only 'currentClass' fields)
            subdataset = subdataset.drop(columns=[bestFeature])
            
            # Check if 'bestFeature' is numeric or nominal
            if numericColumn == True:
                # If numeric, comparisonFormula is the value that splits
                # numerical values in two classes (i.e. is the x
                # in <= x or >x comparison) taken with '<='
                # comparison aign at the beggining (it is converted
                # to such form in the findDecision() method)
                comparisonFormula = currentClass
            else:
                # If nominal, the comparison present in the rule set
                # (identification tree) will be comparison to string
                comparisonFormula = f" == '{currentClass}'"
            
            #------------------------------------------#
            #-------- If terminal node reached --------#
            #------------------------------------------#

            terminateBuilding = False
            
            #----- Only one target class left ----# 
            if len(subdataset['Target'].value_counts().tolist()) == 1:
                # Get the only class left
                finalTarget = subdataset['Target'].value_counts().keys().tolist()[0]
                leaf = IDTreeLeaf(finalTarget)
                terminateBuilding = True

            #---------- No features left ---------#
            # Cannot decide basing on training data
            # no features left despite of more than
            # one target class
            elif subdataset.shape[1] == 1:
                # Get most common class
                finalTarget = subdataset['Target'].value_counts().idxmax()
                leaf = IDTreeLeaf(finalTarget)
                terminateBuilding = True
            
            #-------------------------------------------#
            #-- Terminate branch or continue building --#
            #-------------------------------------------#
            
            # If terminal node (leaf) found
            if terminateBuilding == True:
                returnNode.addChild(comparisonFormula, leaf)
            
            # If decision is not made, continue to create branch and leafs
            else: 
                node = self.__buildTree(subdataset, featuresTypes)
                returnNode.addChild(comparisonFormula, node)

        return returnNode




    def __convertToNominal(self, df, featureName, entropy):
        """ Converts numerical feature into nominal feature in an optimal way
        
        Parameters
        ---------
        df : pandas.DataFrame
            data set to analyse features for.
            TAKE CARE: df is muted during computation so pass
            copy of original data to avoid it's loss
        featureName : string
            name of the numerical feature to convert
        entropy : double
            entropy of the whole df data set with respect to Target

        Returns
        -------
        df : pandas.DataFrame
            converted df set

        """

        # Get number of unique numerical values - sort it ascending
        uniqueFeaturesValues = sorted(df[featureName].unique())
        
        subsetGains = []
        subsetGainratios = []
        subsetGinis = []
        
        # If one numerical value we can create a single class
        if len(uniqueFeaturesValues) == 1:
            # The only threshold possible
            bestFeatureThreshold = uniqueFeaturesValues[0]
            # Format all numerical classes to two (<=x and >x) nominal classes
            df[featureName] = \
                np.where( 
                    df[featureName] <= bestFeatureThreshold,
                    " <= "+str(bestFeatureThreshold),
                    " > "+str(bestFeatureThreshold)
                )

            return df
        

        #--------------------------(for loop)---------------------------#
        #----- Find entropies/impurities of particular border split ----#
        #---------------------------------------------------------------#

        for i in range(0, len(uniqueFeaturesValues)-1):
            
            # Actually tested border
            actualThreshold = uniqueFeaturesValues[i]
            
            # Split data into two subsets depending on actual border
            subsetOne = df[df[featureName] <= actualThreshold]
            subsetTwo = df[df[featureName] > actualThreshold]
            # Take number of samples (rows) in subsets and whole df
            subsetOneSamples = subsetOne.shape[0]
            subsetTwoSamples = subsetTwo.shape[0]
            totalSamples = df.shape[0]
            # Calculate proportional participation of samples in both classes
            subsetOneProbability = subsetOneSamples / totalSamples
            subsetTwoProbability = subsetTwoSamples / totalSamples
            
            #----- Information Gain -----#
            if self.__entropyIndicator == 'gain':
                actualThresholdGain = entropy - subsetOneProbability * self.__calculateEntropy(subsetOne) \
                                              - subsetTwoProbability * self.__calculateEntropy(subsetTwo)
                subsetGains.append(actualThresholdGain)

            #-- Information Gain Ratio --#
            if self.__entropyIndicator == 'gainRatio':
                actualThresholdSplitinfo = - subsetOneProbability * math.log(subsetOneProbability, 2) \
                                           - subsetTwoProbability * math.log(subsetTwoProbability, 2)
                gainratio = actualThresholdGain / actualThresholdSplitinfo
                subsetGainratios.append(gainratio)

            #-------- Gini Index --------#
            elif self.__entropyIndicator == 'gini':
                # Number of decision classes for both feature's classes
                targetsForSubsetOne = subsetOne['Target'].value_counts().tolist()
                targetsForSubsetTwo = subsetTwo['Target'].value_counts().tolist()

                # Initial ginis for both classes
                subsetOneGini = 1
                subsetTwoGini = 1

                # Gini value for 1st class
                for j in range(0, len(targetsForSubsetOne)):
                    subsetOneGini = subsetOneGini - math.pow((targetsForSubsetOne[j] / subsetOneSamples),2)
                # Gini value for 2nd class
                for j in range(0, len(targetsForSubsetTwo)):
                    subsetTwoGini = subsetTwoGini - math.pow((targetsForSubsetTwo[j] / subsetTwoSamples),2)

                # Total gini value for particular border
                gini = (subsetOneSamples / totalSamples) * subsetOneGini + \
                       (subsetTwoSamples/totalSamples) * subsetTwoGini
                subsetGinis.append(gini)

                
        #---------------------(for loop ends)---------------------#
        #----- Choose the best split and return formated df ------#
        #---------------------------------------------------------#
        
        if self.__entropyIndicator == 'gain':
            bestFeatureThresholdIndex = subsetGains.index(max(subsetGains))
        elif self.__entropyIndicator == 'gainRatio':
            bestFeatureThresholdIndex = subsetGainratios.index(max(subsetGainratios))
        elif self.__entropyIndicator == 'gini':
            bestFeatureThresholdIndex = subsetGinis.index(min(subsetGinis))
        
        # The best threshold possible
        bestFeatureThreshold = uniqueFeaturesValues[bestFeatureThresholdIndex]
        # Format all numerical classes to two (<=x and >x) nominal classes
        df[featureName] = np.where(
            df[featureName] <= bestFeatureThreshold,
            " <= "+str(bestFeatureThreshold),
            " > "+str(bestFeatureThreshold)
        )
        
        return df