import pandas as pd
from idtrees.ID3 import ID3
from idtrees.C45 import C45



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
df = pd.read_csv('datasets/student-mat.csv')
df = ID3.prepareData(df, 'Mjob', features=['school' ,'sex' ,'age' ,'address' ,'famsize' ,'Pstatus' ,'Medu' ,'Fedu' ,'Fjob' ,'reason' ,'guardian' ,'traveltime' ,'studytime' ,'failures' ,'schoolsup' ,'famsup' , 'paid', 'activities'])

# Build identification tree
algorithm = ID3(entropyIndicator='gain')
tree_ID3 = algorithm.compute(df)

# Build identification tree
algorithm = C45(entropyIndicator='gain')
tree_C45 = algorithm.compute(df)

# Serialize tree to function
tree_ID3.saveAsFunction('rule_ID3.py')
tree_C45.saveAsFunction('rule_C45.py')

# Collect accuracy statistic (on training set) for ID3
count = 0
for i in range(df.shape[0]):
    sample = df.iloc[i].tolist()
    if tree_ID3.predict(sample[:len(sample) - 1]) == sample[len(sample) - 1]:
        count = count + 1
print(f"ID3: {count/df.shape[0]*100}%")

# Collect accuracy statistic (on training set) for C45
count = 0
for i in range(df.shape[0]):
    sample = df.iloc[i].tolist()
    if tree_C45.predict(sample[:len(sample) - 1]) == sample[len(sample) - 1]:
        count = count + 1
print(f"C45: {count/df.shape[0]*100}%")