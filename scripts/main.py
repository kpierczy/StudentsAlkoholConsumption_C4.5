import pandas as pd
from idtrees.ID3 import ID3
from idtrees.C45 import C45
import math

def AccuracyTesting(tree,testingSet) :
    count = 0
    for i in range(testingSet.shape[0]):
        sample = testingSet.iloc[i].tolist()
        if tree.predict(sample[:len(sample) - 1]) == sample[len(sample) - 1]:
            count = count + 1
    #print(f"ID3: {count/testingSet.shape[0]*100}%")
    return count/testingSet.shape[0]*100

def Kvalidation(data,k):
    df=data.sample(frac=1).reset_index(drop=True)
    numerousness = math.floor(len(df.index)/k)
    lower_limit = - numerousness
    upper_limit = -1
    print(numerousness)
    #learningSet = 0
    #testingSet = 0

    for i in range(0,k):
        lower_limit = lower_limit + numerousness
        upper_limit = upper_limit + numerousness
        
        #choosing subset as testing set
        testingSet = df.loc[lower_limit:upper_limit]
        
        #choosing indices to delete ( testing set ) 
        deleteIndices = [index for index in range(lower_limit,upper_limit+1)]
        learningSet =  df.drop(deleteIndices)
        
        #reset indices to be from 0 to ... without gaps
        learningSet.index = range(len(learningSet))
        testingSet.index = range(len(testingSet))

        # Build identification tree
        algorithm = ID3(entropyIndicator='gain')
        tree_ID3 = algorithm.compute(learningSet)

        # Build identification tree
        algorithm = C45(entropyIndicator='gain')
        tree_C45 = algorithm.compute(learningSet)

        tree_ID3.saveAsFunction('rule_ID3.py')
        tree_C45.saveAsFunction('rule_C45.py')

        # we calculate the error
        ID3_result = AccuracyTesting(tree_ID3,testingSet)
        C45_result = AccuracyTesting(tree_C45,testingSet)

        # show results
        print("kolejka nr ",i," | Error ID3 : ",ID3_result," | Error C45 : ",C45_result)
        
        
    
###############################################################
# 
# TODO description: 'TODO' hashes are placed in files where 
# something is to do yet:
#
#  1) No (*) after 'TODO' means, that it is obligatory for
#     us to do.
#
#   2) Single (*) after 'TODO' means, that we should do it,
#     as it is part of the C4.5 algorithm, but it is not
#     implemented in every case, so we are also not obliged
#     to
#  
#  3) Double (*) after 'TODO' means, that it would be nice
#     if we did it (as it is just cool feature), but we
#     don't have to
#
###############################################################



#-------------------------------------------------------------#
#----------------------- TODO - Tests ------------------------#
#-------------------------------------------------------------#
#
# To conduct tests we need to switch Dalc/Walc features from
# numerical to nominal (ID3 and C4.5 are designed for
# classification purpose and not for regression.
#  1) we can switch [1..5] range to [very_low...very_high]
#  2) it's easy to do with pandas
#
# Tests should incorporate:
#  1) Cross-validation learning (sklearn has suitable classes)
#  2) Comparison between different entropy/impurity indicators
#  3) Comparison between ID3 and C4.5
#



###############################################################
#------ Example of ID3 \usage (run it from root folder) -------#
###############################################################

# Prepare data - read ID3 class' header comment
# to find out why data have to be prepared
pd.set_option('display.max_rows', 100)

df = pd.read_csv('datasets/student-mat.csv')
df = ID3.prepareData(df, 'Dalc', features=['school' ,'sex' ,'age' ,'address' ,'famsize' ,'Pstatus' ,'Medu' ,'Fedu' ,'Fjob' ,'reason' ,'guardian' ,'traveltime' ,'studytime' ,'failures' ,'schoolsup' ,'famsup' , 'paid', 'activities'])

Kvalidation(df,8)

# Build identification tree
#algorithm = ID3(entropyIndicator='gain')
#tree_ID3 = algorithm.compute(df)

# Build identification tree
#algorithm = C45(entropyIndicator='gain')
#tree_C45 = algorithm.compute(df)

# Serialize tree to function
#tree_ID3.saveAsFunction('rule_ID3.py')
#tree_C45.saveAsFunction('rule_C45.py')

# Collect accuracy statistic (on training set) for ID3
#count = 0
#for i in range(df.shape[0]):
#    sample = df.iloc[i].tolist()
#    if tree_ID3.predict(sample[:len(sample) - 1]) == sample[len(sample) - 1]:
#        count = count + 1
#print(f"ID3: {count/df.shape[0]*100}%")

#AccuracyTesting(tree_ID3,df)

# Collect accuracy statistic (on training set) for C45
#count = 0
#for i in range(df.shape[0]):
#    sample = df.iloc[i].tolist()
#    if tree_C45.predict(sample[:len(sample) - 1]) == sample[len(sample) - 1]:
#        count = count + 1
#print(f"C45: {count/df.shape[0]*100}%")


