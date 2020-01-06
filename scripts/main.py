import pandas as pd
from ID3 import ID3

algorithm = ID3()
df = pd.read_csv('StudentsAlkoholConsumption_C4.5/datasets/student-mat.csv')
df = algorithm.prepareData(df, 'Mjob', features=['age', 'Medu', 'Fedu', 'Dalc', 'Walc', 'health', 'absences'])
tree = algorithm.compute(df)
tree.saveAsFunction('rule.py')