# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 09:29:07 2019

@author: loren
"""

import csv
import pandas as pd
from datetime import datetime,date


with open ('reddit_exercise_data.csv','r',encoding='utf-8') as file:
    csv_reader=csv.reader(file)
    with open('test.csv','w',encoding='utf-8') as new_file:
         csv_writer=csv.writer(new_file,delimiter=',',quoting=csv.QUOTE_ALL)
  
         for line in csv_reader:
            csv_writer.writerow(line)
            
# import the data            
df = pd.read_csv('test.csv')
# drop the  columns
df=df.drop(['product_name'],axis=1)
df=df.drop(['review'],axis=1)
df=df.rename(columns=({'app_bought':'apps_bought'}))

def trim(df):
    trim = lambda x: x.strip() if type(x) is str else x
    return df.applymap(trim)

#checking the number of empty rows in th csv file
print (df.isnull().sum())


df.dropna(thresh=3)
df.money_spent = df.money_spent.fillna(df.money_spent.mean())
df.money_spent = df.money_spent.fillna(df.apps_bought.mean())

 # convert the 'Date' column into datetime
df['date']=pd.to_datetime(df['date'], utc=False).dt.date
def date_to_weekday(date_value):
    return date_value.weekday()
df['day_of_the_week']=df['date'].apply(date_to_weekday)

 # create two columns with variables available in buckets
df['apps_bought'] = df['apps_bought'].astype(float)
df['money_spent'] = df['money_spent'].astype(float)
df['apps_bought_bucket'] = pd.cut(df['apps_bought'],[0, 50, 100], labels=['0-50', '50-100'])
df['money_spent_bucket'] = pd.cut(df['money_spent'],[0, 250, 500], labels=['0-250', '250-500'])
df.apps_bought_bucket = df.apps_bought_bucket.fillna('0-50')
df.money_spent_bucket = df.money_spent_bucket.fillna('0-250')
df['apps_bought_bucket'] = df['apps_bought_bucket'].astype(str)
df['money_spent_bucket'] = df['money_spent_bucket'].astype(str)

#sorting by money_spent
df.sort_values(by='money_spent',ascending=0,inplace=True)

#removing unwanted "
df.loc[df['title'].str.contains('"'), 'title'] = ''
df.loc[df['title'].str.contains('\''), 'title'] = '\''


df.to_csv('Final.csv', index=False)



