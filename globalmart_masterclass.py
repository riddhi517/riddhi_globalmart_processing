# -*- coding: utf-8 -*-
"""globalmart_masterclass.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IpmuDqqs94DY5QmZxN60kgw7juqJ258v
"""

pip install pandas

pip install requests

import requests
response = requests.get('https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales?offset=1&limit=100', headers= {"access_token":"fe66583bfe5185048c66571293e0d358"})

response

print("Content:", response.text)

print("Status code:", response.status_code)
print(response.raise_for_status())

data=response.json()

import pandas as pd
import json
df1 = pd.DataFrame(data)
df1

import requests
response = requests.get('https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales?offset=101&limit=200', headers= {"access_token":"fe66583bfe5185048c66571293e0d358"})

data=response.json()

df2 = pd.DataFrame(data)
df2

import requests
response = requests.get('https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales?offset=201&limit=300', headers= {"access_token":"fe66583bfe5185048c66571293e0d358"})

data=response.json()

df3 = pd.DataFrame(data)
df3

import requests
response = requests.get('https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales?offset=301&limit=400', headers= {"access_token":"fe66583bfe5185048c66571293e0d358"})

data=response.json()

df4 = pd.DataFrame(data)
df4

import requests
response = requests.get('https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales?offset=401&limit=500', headers= {"access_token":"fe66583bfe5185048c66571293e0d358"})

data=response.json()

df5 = pd.DataFrame(data)
df5

dataframes_to_concat = [df1,df2,df3,df4,df5]
df_final = pd.concat(dataframes_to_concat, ignore_index=True)

data_df = df_final['data']
data_df = pd.json_normalize(data_df)
data_df

data_df.head(5)

data_df.isnull().sum()

data_df.duplicated().sum()

data_df['order.order_purchase_date']=pd.to_datetime(data_df['order.order_purchase_date'])
data_df['day_of_order'] =data_df['order.order_purchase_date'].dt.dayofweek
data_df

data_df['order.order_purchase_date']=pd.to_datetime(data_df['order.order_purchase_date'])
data_df['day_of_order'] = data_df['order.order_purchase_date'].dt.dayofweek

def get_day_label(day_of_order):
  if day_of_order < 5:
    return 'weekday'
  else:
    return 'weekend'

data_df['day_label'] = data_df['day_of_order'].apply(get_day_label)
data_df

num_weekend_orders = data_df[data_df['day_label']=='weekend'].shape[0]
num_weekend_orders

weekday_data = data_df[data_df['day_label'] == 'weekday']
weekend_data = data_df[data_df['day_label'] == 'weekend']

weekday_sales_sum = weekday_data['sales_amt'].sum()
weekend_sales_sum = weekend_data['sales_amt'].sum()

# Compare the sales and find the highest
highest_sales_group = 'weekday' if weekday_sales_sum > weekend_sales_sum else 'weekend'
highest_sales_group

sales_by_category = data_df.groupby('product.category')['sales_amt'].sum()

highest_sales_category = sales_by_category.idxmax()
highest_sales_category

"""TASK:1 Determine which product has the maximum sizes available."""

def str_split(s):
  return len(s.split(','))

data_df['lenn'] = data_df['product.sizes'].apply(str_split)

data_df['lenn'].max()

print(data_df['product.product_name'].loc[data_df['lenn'] == (56)])

"""Task: 2 Select how many sizes are available for the product Mitel 5320 IP Phone VoIP phone."""

data_df['lenn'].loc[data_df['product.product_name'] == ('Mitel 5320 IP Phone VoIP phone')]

"""Task 3: Which month had the highest sales overall?"""

data_df['month'] = data_df['order.order_purchase_date'].apply(lambda date:date.strftime('%B'))

monthly_sales=data_df.groupby('month')['sales_amt'].sum()
print('highest sale by month:',monthly_sales.idxmax())

"""
Task: 4 Which month had the highest overall profit?"""

monthly_profit = data_df.groupby('month')['profit_amt'].sum()
monthly_profit.sort_values()

"""Task:5 how many months have lead to a positive profit margin?"""

num_positive_months=(monthly_profit>0).sum()
print('No. of months with positive monthly profit:',num_positive_months)

"""Task 6: How many orders are late delivered to the customers?"""

data_df.replace('null',None,inplace=True)
data_df.isnull().sum()

data_df['order.order_purchase_date']=pd.to_datetime(data_df['order.order_purchase_date'])
data_df['order.order_approved_at']=pd.to_datetime(data_df['order.order_approved_at'])
data_df['order.order_delivered_carrier_date']=pd.to_datetime(data_df['order.order_delivered_carrier_date'])
data_df['order.order_delivered_customer_date']=pd.to_datetime(data_df['order.order_delivered_customer_date'])
data_df['order.order_estimated_delivery_date']=pd.to_datetime(data_df['order.order_estimated_delivery_date'])

data_df['delay']=  (data_df['order.order_delivered_customer_date']- data_df['order.order_estimated_delivery_date']).dt.days

data_df['delay_status'] = data_df['delay'].apply(lambda x: 'Late' if x>0 else('Early' if x<0 else 'On Time'))

data_df['delay_status'].value_counts()

"""Task7 : Which vendor has the highest late deliveries?"""

late_df = data_df[data_df['delay_status']=='Late']

vendor_late_delivery_count = late_df.groupby('order.vendor.VendorID')['id'].count()
print('vendor with most late deliveries:',vendor_late_delivery_count.idxmax())

vendor_late_delivery_count