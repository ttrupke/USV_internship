# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 10:44:31 2019

@author: T011978
"""

import pandas as pd
import numpy as np
import re
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#read in file and label the expenses columns
df = pd.read_excel("")

expense_columns = ['Accounting Expenses', 'Advertising Expense', 'Computer Expenses', 'Contract Labor Expenses',
           'Insurance Expenses', 'Legal Expenses', 'Management/Administration Expenses', 'Office Supplies Expenses',
           'Package/Container Expenses', 'Payroll and Benefits Expenses', 'Purchase Print Expenses', 'Rent Expenses',
           'Telcom Expenses', 'Transportation Expenses', 'Utilities Expense']

#strip the expense columns to get the dollar value from them, rather than a text string
for column in expense_columns:
    temp = df[column]
    temp.fillna("$0", inplace=True)

#regex expression to find dollar values
    temp_list = []
    for x in range(len(temp)):
        cur = re.findall(r"(?:\£|\$|\€)(?:[\d\.\,]{1,})",temp[x])
        first_cur = cur[0]
        temp_list.append(first_cur)

    raw_list = pd.Series(data = temp_list)

    raw_list = raw_list.str.replace(',', '')
    raw_list = raw_list.str.replace('$', '')
    raw_list = raw_list.astype("float64")
    
#label the values, since '1 million' refers to 1,000,000, among others    
    raw_list.where(cond = raw_list != 1, other = 1000000, inplace=True)
    raw_list.where(cond = raw_list != 2.5, other = 2500000, inplace=True)
    raw_list.where(cond = raw_list != 10, other = 10000000, inplace=True)
    raw_list.where(cond = raw_list != 0, other = np.median(raw_list), inplace=True)
    
    df[column] = raw_list

#do a similar process to strip the square footage column down to a float value
sqft = df['Square Footage']
sqft = sqft.str.replace(',', '')

sqft_list = []

for y in range(len(sqft)):
    num = re.findall("\d+", sqft[y])
    first_num = num[0]
    sqft_list.append(first_num)
    
sqft_col = pd.Series(data = sqft_list)
sqft_col = sqft_col.astype("float64")
df['Square Footage'] = sqft_col

data = pd.DataFrame()

#drop data which isn't a float or an int, so we only have numerical data. this is why we were stripping down the expense columns
data = df.select_dtypes(include = ['float64', 'int64'])

data['Total Expenses'] = df[expense_columns].sum(axis=1)

#drop irrelevant columns not needed in the clustering model
data.drop(['Miles to warehouse', 'Professional Title', 'Mailing Zip Code', 'Mailing Zip 4', 'Mailing Delivery Point Barcode',
           'Location ZIP Code', 'Location ZIP+4', 'Location Address Delivery Point Barcode', 'Latitude', 'Longitude', 
           'Corporate Employee Size Actual', 'Corporate Sales Volume Actual', 'Year Appeared 1', 'Primary NAICS Code', 
           'NAICS 1', 'Franchise Code 2', 'Cuisine Type', 'Holding Status', 'Fortune 1000 Ranking', 'Infogroup ID',
           'Parent Infogroup ID', 'EIN 1', 'EIN 2', 'EIN 3', 'Lead Status', 'Tags',  'Franchise/Specialty Code 2.1',
           'Franchise3_0', 'Franchise3_1', 'Franchise4_0', 'Franchise4_1', 'Franchise5_0', 'Franchise5_1', 'Franchise6_0',
           'Franchise6_1', 'Affiliated Records', 'Affiliated Locations', 'Year Established', 'NAICS'], axis=1, inplace=True)
data.drop(columns = expense_columns, inplace=True)
data.fillna(0, inplace=True)
   
#if the data is missing, fill in with the median values 
data['Location Sales Volume Actual'].where(cond = data['Location Sales Volume Actual'] != 0, 
    other = np.median(data['Location Sales Volume Actual']), inplace=True)
data['Location Employee Size Actual'].where(cond = data['Location Employee Size Actual'] != 0, 
    other = np.median(data['Location Employee Size Actual']), inplace=True)

#X = np.array(data)

#kmeans = KMeans(n_clusters=3)

#kmeans = kmeans.fit(X)

#labels = kmeans.predict(X)

#centroids = kmeans.cluster_centers_

#data['Cluster Number'] = labels

#data = data.where(cond = data['Cluster Number'] == 0)

#get rid of the large companies to remove outliers
data = data.where(cond = data['Location Employee Size Actual'] < 250)
data = data.dropna()
#data.drop(columns = ['Cluster Number'], inplace = True)

#take the log of two columns with very large deviation
X = np.array(data)
X[:,1] = np.log(X[:,1])
X[:,3:] = np.log(X[:,3:])

#perform Kmeans clustering
kmeans = KMeans(n_clusters=4, init='k-means++')
Kmeans = kmeans.fit(X)
labels = kmeans.predict(X)
centroids = kmeans.cluster_centers_


# plt.scatter(Y[:, 0], Y[:, 1], c=labels_y, s=50, cmap='viridis')

# plt.scatter(centroids_y[:, 0], centroids_y[:, 1], c='black', s=200, alpha=0.5);

#plot the figure with the colors based on which cluster it is in
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels)
ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], c='#050505', s=100)
           
centroids[:,1] = np.exp(centroids[:,1])
centroids[:,3:] = np.exp(centroids[:,3:])

centroids_final = pd.DataFrame(data=centroids, columns = data.columns)

data['Cluster Number'] = labels










