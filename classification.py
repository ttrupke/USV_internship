# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 15:57:53 2019

@author: T011978
"""

import pandas as pd


df = pd.read_csv('', index_col='Unnamed: 0')

df.drop_duplicates(subset=['Company Name', 'Miles to warehouse'], inplace=True)

columns = df.columns.tolist()
na_list = []
for column in columns:
    count = df[column].isna().sum()
    na_list.append(count)
    
df_na = pd.DataFrame()
df_na['colnames']=columns
df_na['count']=na_list

df2 = df.copy()

for index, row in df_na.iterrows():
    if row['count']>75:
        df2.drop(columns=row['colnames'], inplace=True)


add_cols = ['taxId','bankruptcyCount','taxLienCount','uccFilings','Company Website']  

for column in add_cols:
      df2[column]=df[column]    

states = {'WI': 1, 'IL': 1, 'IN': 1, 'MO': 1, 'KS': 1, 'NE': 1, 'SD': 1,
          'ND': 1, 'IA': 1, 'MN': 1, 'TX': 2, 'MI': 2, 'OH': 2, 'PA': 2}

df2['foot_ind'] = df2['Location State'].map(states)
df2['foot_ind'] = df2['foot_ind'].fillna(0)

footprint = {0: 'Outside of footprint', 1: 'Within footprint', 2: 'Next 3-5 years'}

df2['foot_desc'] = df2['foot_ind'].map(footprint)

df2.to_csv('')


