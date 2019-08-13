# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 12:29:03 2019

@author: T011978
"""

import os
import pandas as pd
import numpy as np
import re
from unidecode import unidecode

folder = ''
listdir = os.listdir(folder)

df = pd.DataFrame()

for object in listdir:
    openfilepath = folder + "/" + object
    flatfile = pd.read_csv(openfilepath)
    flatfile.set_index('Key', inplace = True)
    flat_tran = flatfile.transpose()

    for column in flat_tran.columns.tolist():
        if column in df.columns:
            pass
        else:
            df[column] = np.nan
            df[column] = df[column].astype('object')
            
    df = df.astype('object')    
    df = pd.merge(df, flat_tran, how = "outer", on = df.columns.intersection(flat_tran.columns).tolist())
    print(object," done")
    
df = df.astype('object')

df.to_csv('')

#pd.set_option('display.float_format', lambda x: '%.3f' % x)

#df = pd.read_csv('')
## can just read in csv from this point from file path above, rather than creating list again

df['phone join'] = df['phone'].str[-10:]
#phone_list = df['phone'].astype('object')

#for item in phone_list:
#    phonum = item.astype('object')

df2 = pd.read_excel('')

phone_list_2 = df2['Phone Number Combined'].tolist()

temp_list_2 = []

for item in phone_list_2:
    phonum_2 = re.sub("\D", "", item)
    temp_list_2.append(phonum_2)

df2['phone join'] = temp_list_2

#final_data = df2.join(df.set_index('phone join'), on='phone join')

## if the phone number is on two records it is double joining and creating four records

#final_data.to_csv('')

#data = pd.read_csv('')

add_list = df['address.street'].tolist()
temp_add_list = []

for item in add_list:
    low_add = unidecode(item)
    low_add = re.sub(' +', ' ', low_add)
    low_add = re.sub('\n', ' ', low_add)
    low_add = low_add.strip().strip('"').strip("'").lower().strip()
    low_add = low_add.replace(" ","")
    temp_add_list.append(low_add)
    
df['address join'] = temp_add_list

add_list_2 = df2['Location Address'].fillna('none').astype('object').tolist()
temp_add_list_2 = []

for item in add_list_2:
    low_add_2 = unidecode(item)
    low_add_2 = re.sub(' +', ' ', low_add_2)
    low_add_2 = re.sub('\n', ' ', low_add_2)
    low_add_2 = low_add_2.strip().strip('"').strip("'").lower().strip()
    low_add_2 = low_add_2.replace(" ","")
    temp_add_list_2.append(low_add_2)
    
df2['address join'] = temp_add_list_2

#name_list = df['businessName'].tolist()
#temp_name_list = []

#for item in name_list:
#    low_name = unidecode(item)
#    low_name = re.sub(' +', ' ', low_name)
#    low_name = re.sub('\n', ' ', low_name)
#    low_name = low_name.strip().strip('"').strip("'").lower().strip()
#    low_name = low_name.replace(" ","")
#    temp_name_list.append(low_name)
    
#df['name join'] = temp_name_list

#name_list_2 = df2['Company Name'].fillna('none').astype('str').tolist()
#temp_name_list_2 = []

#for item in name_list_2:
#    low_name_2 = unidecode(item)
#    low_name_2 = re.sub(' +', ' ', low_name_2)
#    low_name_2 = re.sub('\n', ' ', low_name_2)
#    low_name_2 = low_name_2.strip().strip('"').strip("'").lower().strip()
#    low_name_2 = low_name_2.replace(" ","")
#    temp_name_list_2.append(low_name_2)
    
#df2['name join'] = temp_add_list_2

data = pd.merge(df2, df, how='left', on='phone join')

data_1 = data[data.businessName.isnull()]
data_1.drop(data_1.columns[182:],axis=1, inplace=True)

#data_1 = pd.merge(data_1,df, how='left', left_on='address join_x', right_on='address join')

#data_2 = data_1[data_1.businessName.isnull()]
data_1 = data_1.reset_index(drop=True)
#data_2.drop(data_2.columns[184:],axis=1, inplace=True)

#data_2 = pd.merge(data_2,df, how='left', left_on='name join_x', right_on='name join')

df_missing = df[df['bin'].isin(data['bin'])==False]
# df_missing.to_csv('')    

man_match = pd.read_csv('')

man_join = data_1.join(man_match.set_index('matchindex'), lsuffix = 'index', rsuffix = 'matchindex')
extra_cols = man_join.columns.difference(data.columns)

man_join.drop(columns = extra_cols, axis=1, inplace=True)

drop_data = data[data.businessName.notna()]
drop_data.drop(columns='phone join', inplace=True)

final_final_data = drop_data.append(man_join, ignore_index=True)

final_final_data.to_csv('')


