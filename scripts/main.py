import pandas as pd
from ID3 import ID3

algorithm = ID3()
df = pd.read_csv('StudentsAlkoholConsumption_C4.5/datasets/student-mat.csv')
df = algorithm.prepareData(df, 'Mjob', features=['sex', 'age', 'address', 'famsize'])
tree = algorithm.compute(df)
print(df)