# -*- coding: utf-8 -*-
"""riddhi_globalmart.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k2JAfvNBavORhUr5X3qoDhLIGPghmdsz
"""

pip install pandas

pip install requests

import requests
response = requests.get('https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales',headers= {"access_token":"fe66583bfe5185048c66571293e0d358"})

response

print("Content:", response.text)

print("Status code:", response.status_code)
print(response.raise_for_status())

data=response.json()

import pandas as pd
import json
df = pd.DataFrame(data)
df

data_df = df['data']
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

