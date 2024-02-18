#Libreries

import pandas as pd 
import os
import numpy as np

##What to do with the data set???
# Eliminate empty subcategories// From line 55 to 69
#Change the currency to pounds// From line 70 to 98
#cheapest and most expensice items  per category// From line 107 to 156
#filter best items and worst per category// From line 157 to 201
#average of each category and get the most expensive category and cheapest one// From line  202 to 212
#creating a colum with the porcentaje of discount and finding witch categories has more discounts// From line  213 to 228



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

df = pd.read_csv('C:/Users/Miguel.Llorente/OneDrive - FleetCor/Desktop/Python_Excercices/Amazon/Amazon.csv')
df.head()
print(df)
df.info()
df.describe()

#####################################

##Eliminate empty subcategories
##Checking teh data i realize there are some subcategories that are empty, i saw in the main document that i download and i realise those categories
# have a total of 1KB of weight, so i will eliminate all of them


nan_df = df[df.isna().any(axis=1)]
nan_df.head()



value_to_drop =['All Books' , 'All English', 'All Hindi', 'All Movies and TV Shows','All Music','All Video Games','Amazon Pharmacy','Blu-ray','Childrens Books','Entertaiment Collectibles', 'Exam Central', 'Fashion Sales and Deals','Fiction Books','Film Songs','Fine Art','Gamming Accessories','Gaming Consoles','Indian Classical','Indian Language Books','International Music','International Toy Store','Kindle eBooks','Pantrv','PC Games','Refurbished and Open Box','School Textbooks','Sports Collectibles','Subcribe and Save','Textbooks','Toys Gifting Store','Video Games Deals']
##value to drop is the list of each document where doesnt have data
df = df[~df['sub_category'].isin(value_to_drop)]


## Change the currency to punds

df['actual_price'] = df['actual_price'].str[1:]#removing the currency symbol
df['discount_price'] = df['discount_price'].str[1:]#removing the currency symbol
df['actual_price'] = pd.to_numeric(df['actual_price'].str.replace(',', ''), errors='coerce')##converting actual_price column in float so i can change to pounds
df['discount_price'] = pd.to_numeric(df['discount_price'].str.replace(',', ''), errors='coerce')##converting discount_price in float

df.info()

df.to_csv('C:/Users/Miguel.Llorente/OneDrive - FleetCor/Desktop/Python_Excercices/PKM Excercice/Amazon Sells_2023/Amazon.csv')##Saving the progress

df = pd.read_csv('C:/Users/Miguel.Llorente/OneDrive - FleetCor/Desktop/Python_Excercices/PKM Excercice/Amazon Sells_2023/Amazon.csv')

df['actual_price'] = df['actual_price']* 0.0095## Today 11/02/24 one indian rupee is equal to 0.0095£ so i multiply to make the change
df.head()#checking if the price change
df['discount_price'] = df['discount_price']* 0.0095
df['actual_price_£'] = df['actual_price'] ## creating a new colum with the pound symbol in the colum
df['discount_price_£'] = df['discount_price']  ## creating a new colum with the pound symbol in the colum



df.drop(['Unnamed: 0'],axis=1,inplace=True)##Dropping extra columns
df.drop(['Unnamed: 0.3'],axis=1,inplace=True)##
df.drop(['actual_price'],axis=1,inplace=True)##
df.drop(['discount_price'],axis=1,inplace= True)##
df.info()
df.head()


##Saving Progress
df.to_csv('C:/Users/Miguel.Llorente/OneDrive - FleetCor/Desktop/Python_Excercices/PKM Excercice/Amazon Sells_2023/Amazon.csv')##Saving the progress
df = pd.read_csv('C:/Users/Miguel.Llorente/OneDrive - FleetCor/Desktop/Python_Excercices/PKM Excercice/Amazon Sells_2023/Amazon.csv')
df.info()
df.head()


###############################################
# ##Most Expensive item and Cheapest

Most_expensive = df.sort_values(['actual_price_£'],ascending=False)
print(Most_expensive)
Most_expensive.head(10)##top 10 most expensive products


## There are some mistakes with the prices of some Items so i will have to remove the first 4 items, i dont think a mosquito killer worth 90 millions pounds

df['refNumb'] = df.index +1##Creating a reference number for each product
df = df[['refNumb'] + [col for col in df.columns if col != 'refNumb']]# moving the new column to the beggining.


df.set_index('refNumb',inplace=True)##making the refNumb  the index column
df.head()


Most_expensive = Most_expensive[Most_expensive['refNumb'] !=2952313]##Dropping products with wrong data
Most_expensive = Most_expensive[Most_expensive['refNumb'] != 223380]
Most_expensive = Most_expensive[Most_expensive['refNumb'] !=2429528]
Most_expensive = Most_expensive[Most_expensive['refNumb'] !=1383958]
Most_expensive = Most_expensive[Most_expensive['refNumb'] !=803669]
Most_expensive = Most_expensive[Most_expensive['refNumb'] !=1906743]

df.head()


cheapest = df.sort_values(['actual_price_£'],ascending=True)
print(cheapest)
cheapest.head(10)##top 10 cheapest Items

######## Cheapest and most expensive item by main category



cheapest_by_category = df.groupby('main_category').apply(lambda x: x.sort_values('actual_price_£', ascending=True))
cheapest_by_category.reset_index(drop=True, inplace=True)
top3_cheapest_by_category = df.groupby('main_category').apply(lambda x: x.nsmallest(3, 'actual_price_£'))
top3_cheapest_by_category.head(12)## top 3 cheapest item per category 





expensive_by_category = df.groupby('main_category').apply(lambda x: x.sort_values('actual_price_£', ascending = False))
expensive_by_category.reset_index(drop=True, inplace=True)
top3_expensive_by_category = df.groupby('main_category').apply(lambda x: x.nlargest(3, 'actual_price_£'))
top3_expensive_by_category.head(12)## top 3 most expensive item per category 


##################################################
###
##Best item by category and worst item by category


#creating some formula to give more value to the prodructs that have more no_of_ratings

def choose_most_rated_product(group):
    # Sort the group by ratings and no_of_ratings in descending order
    sorted_group = group.sort_values(['ratings', 'no_of_ratings'], ascending=[False, False])
    
    # Select the first row (most rated) from the sorted group
    most_rated_product = sorted_group.iloc[0]
    
    return most_rated_product

# Assuming df is your DataFrame
best_by_category = df.groupby('main_category').apply(lambda x: x.sort_values('actual_price_£', ascending=False))
best_by_category.reset_index(drop=True, inplace=True)

# Find the most rated product within each 'main_category'
most_rated_by_category = df.groupby('main_category').apply(choose_most_rated_product)

# Reset the index after grouping
most_rated_by_category.reset_index(drop=True, inplace=True)

# Display the most rated products
print(most_rated_by_category.head())
most_rated_by_category.head()



df['ratings'] = df['ratings'].str.extract('(\d+)', expand=False).astype(float)
df['no_of_ratings'] = df['no_of_ratings'].str.extract('(\d+)', expand=False).astype(float)

df = df[df['ratings'] <= 5]


best_by_category = df.groupby('main_category').apply(lambda x: x.sort_values('actual_price_£', ascending = False))
best_by_category.reset_index(drop=True, inplace=True)
top3_best_by_category = df.groupby('main_category').apply(lambda x: x.nlargest(3, 'actual_price_£'))
top3_best_by_category.head(12)## top 3 most expensive item per category 



###################################
#average of each category and get the most expensive category and cheapest one

df.head()

average_category = df.groupby('main_category')['actual_price_£'].mean()##average of each category
average_category.sort_values(ascending=False)## filtered by most expensive to cheapest one
##Expensiest categories are Home & kitchen, accesories, appliances



####################################
#creating a colum with the porcetaje of discount and finding witch categories has more discounts


df.head()

df['%_discount'] = ((df['actual_price_£'] - df['discount_price_£']) / df['actual_price_£']) * 100##getting the porcentaje we will pay
df['%_discount'] = df['%_discount']- 100# getting the porcentaje we will discount
df['%_discount'] = df['%_discount'] * -1# making that porcenatje a positive number
df.head()#checking

porcentaje_by_category = df.groupby('main_category')['%_discount'].max()
print(porcentaje_by_category)
porcentaje_by_category.sort_values(ascending=False)##Max porcentaje per category


#######################################









