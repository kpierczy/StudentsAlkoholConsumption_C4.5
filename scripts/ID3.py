import math
import numpy as np

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
        entropyIndicator : {'gain', 'gainRatio', 'gini'}, optional (default : 'gain)
            method of measuring entropy/impurity of computed
            feature/target classes
        """
        self.__entropyIndicator = entropyIndicator
        pass




    ###########################################################################################
    #############################  Configuration interface  ###################################
    ###########################################################################################

    def getEntropyIndicator(self):
        """ Returns actual entropyIndicator"""
        return self.__entropyIndicator

    def setEntropyIndicator(self, entropyIndicator):
        """ Sets a new value for entropyIndicator 
        
        Parameters
        ---------
        entropyIndicator : {'gain', 'gainRatio', 'gini'}
            method of measuring entropy/impurity of computed
            feature/target classes
        
        Returns
        -------
        False : bool
            wrong entropyIndicator given
        True : bool
            new entropyIndicator set
        """
        
        if entropyIndicator in {'gain', 'gainRatio', 'gini'}:
            self.__entropyIndicator = entropyIndicator
            return True
        else:
            return False




    ###########################################################################################
    ####################################  Algorithm  ##########################################
    ###########################################################################################

    def compute(self, df):
        pass




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
        # Get number of instances and number of classes in the target
        instances = df.shape[0]
        targetClasses = df['Target'].value_counts().keys().tolist()
        entropy = 0

        # Calculate and sum elements of entropy for every class
        for i in range(0, len(targetClasses)):
            num_of_decisions = df['Decision'].value_counts().tolist()[i]		
            classProbability = num_of_decisions/instances
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
                # Get rows (samples) where feature is equal to 'current_class'
                subdataset = df[df[featureName] == currentClass]
                # Count number of samples in 'current_class'
                subsetSamplesNumber = subdataset.shape[0]
                # Calculate ratio of the samples present in 'current_class'
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
            beastFeatureIndex = gains.index(max(gains))
        elif self.__entropyIndicator == 'gainRatio':
            beastFeatureIndex = gainratios.index(max(gainratios))
        elif self.__entropyIndicator == 'gini':
            beastFeatureIndex = ginis.index(min(ginis))

        beastFeatureName = df.columns[beastFeatureIndex]
        return beastFeatureName




    def __buildTree(self, df):
        pass




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
                np.where( \
                    df[featureName] <= bestFeatureThreshold, \
                    "<="+str(bestFeatureThreshold), \
                    ">"+str(bestFeatureThreshold) \
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
            total_instances = df.shape[0]
            # Calculate proportional participation of samples in both classes
            subsetOneProbability = subsetOneSamples / total_instances
            subsetTwoProbability = subsetTwoSamples / total_instances
            
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
                gini = (subsetOneSamples / total_instances) * subsetOneGini + \
                       (subsetTwoSamples/total_instances) * subsetTwoGini
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
        df[featureName] = np.where( \
            df[featureName] <= bestFeatureThreshold, \
            "<="+str(bestFeatureThreshold), \
            ">"+str(bestFeatureThreshold) \
        )
        
        return df