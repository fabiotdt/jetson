import pandas as pd

# Load the csv file using pandas' read_csv() function
df = pd.read_csv('/home/fabio_tdt/Desktop/Data_measurments/dataset/dataset.csv')

# Display the loaded csv file as a pandas dataframe using the print() functiond

print(df.head())