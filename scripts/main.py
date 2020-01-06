import pandas as pd
from idtress.ID3 import ID3

# Prepare data
df = pd.read_csv('StudentsAlkoholConsumption_C4.5/datasets/student-mat.csv')
df = ID3.prepareData(df, 'Mjob') #, features=['age', 'Medu', 'Fedu', 'Dalc', 'Walc', 'health', 'absences'])

# Compute algorithm
algorithm = ID3(entropyIndicator='gain')
tree = algorithm.compute(df.copy())

# Serialize tree to function
tree.saveAsFunction('rule.py')

# Collect accuracy statistic
count = 0
for i in range(df.shape[0]):
    print(i)
    sample = df.iloc[i].tolist()
    if tree.predict(sample[:len(sample) - 1]) == sample[len(sample) - 1]:
        count = count + 1

print(f"{count}/{df.shape[0]}")
