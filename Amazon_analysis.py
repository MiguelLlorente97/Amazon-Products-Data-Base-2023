#Libreries

import pandas as pd 
import os
import numpy as np

##What to do with the data set
# Eliminate empty subcategories
#Change the currency to pounds
#filter best items and worst per category, subcategory




##importing dataset

###############################
##Creating a single document that content all other document together
path = r'C:/Users/Miguel.Llorente/OneDrive - FleetCor/Desktop/Python_Excercices/Amazon'

df = pd.DataFrame()

for archive in os.listdir(path):
    if archive.endswith('.csv'):
        archive_path = os.path.join(path,archive)
        
        
        df_temporal = pd.read_csv(archive_path)
        df = pd.concat([df, df_temporal],ignore_index=True,sort=False)
        
df.to_csv(r'C:/Users/Miguel.Llorente/OneDrive - FleetCor/Desktop/Python_Excercices/Amazon/Amazon.csv')##saving that document 

#########################################
##Creating the DataFrame

df = pd.read_csv('C:/Users/Miguel.Llorente/OneDrive - FleetCor/Desktop/Python_Excercices/PKM Excercice/Amazon Sells_2023/Amazon.csv')
print(df)
df.info()
df.describe()

#####################################
##Data Wraling

##Eliminate empty subcategories
##Checking teh data i realize there are some subcategories that are empty, i saw in the main document that i download and i realise those categories
# have a total of 1KB of weight, so i will eliminate all of them

value_to_drop =['All Books' , 'All English', 'All Hindi', 'All Movies and TV Shows','All Music','All Video Games','Amazon Pharmacy','Blu-ray','Childrens Books','Entertaiment Collectibles', 'Exam Central', 'Fashion Sales and Deals','Fiction Books','Film Songs','Fine Art','Gamming Accessories','Gaming Consoles','Indian Classical','Indian Language Books','International Music','International Toy Store','Kindle eBooks','Pantrv','PC Games','Refurbished and Open Box','School Textbooks','Sports Collectibles','Subcribe and Save','Textbooks','Toys Gifting Store','Video Games Deals']
##value to drop is the list of each document where doesnt have data
df = df[~df.isin([value_to_drop]).any(axis=1)]


## Change the currency to punds


df['actual_price'] = pd.to_numeric(df['actual_price'],errors='coerce')##converting actual_price column in float so i can change to pounds
df['discount_price'] = pd.to_numeric(df['discount_price'],errors='coerce')##converting discount_price in float
df.info()








