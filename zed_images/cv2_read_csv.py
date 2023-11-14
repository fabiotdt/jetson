import pandas as pd

# Load the csv file using pandas' read_csv() function
df = pd.read_csv('/home/fabio_tdt/Desktop/Data_measurments/dataset/dataset.csv') # Linux
#df = pd.read_csv('C:\\Users\\fabio\\Desktop\\Data_measurments\\dataset\\dataset.csv') # Windows
# Data quality
#df = pd.read_csv('C:\\Users\\fabio\\Desktop\\Data_quality\\dataset\\dataset.csv') # Windows
#df = pd.read_csv('/home/fabio_tdt/Desktop/Data_measurments/dataset/dataset.csv') # Linux
# Display the loaded csv file as a pandas dataframe using the print() functiond

print(df.head())