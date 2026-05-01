
average order value.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

orders=pd.read_csv('data/orders.csv')
order_items=pd.read_csv('data/order_items.csv')

df1=orders.merge(order_items,how='left',on='order_id')
pd.set_option('display.max_column',None)
print(df1)
print(df1.info())
print(df1.isna().any())
print(df1[['unit_price','quantity','discount_amount']].describe())
print(df1['order_id'].duplicated().any())

df1['revenue']=df1['unit_price']*df1['quantity']
order_level_1 = df1.groupby(['order_id','order_source','device_type','payment_method'])['revenue'].sum().reset_index()
order_level_1.groupby('order_source')['revenue'].agg(['count','mean','median'])
order_level_1.groupby('device_type')['revenue'].agg(['count','mean','median'])
order_level_1.groupby('payment_method')['revenue'].agg(['count','mean','median'])
df1.groupby('product_id')['revenue'].agg(['sum','mean','count'])
sns.boxplot(data=order_level_1, x='order_source', y='revenue')
plt.title('AOV Distribution by Order Source')
plt.xlabel('Order Source')
plt.ylabel('Order Value')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.show()
sns.boxplot(data=order_level_1, x='device_type', y='revenue')
plt.title('AOV Distribution by Device Type')
plt.xlabel('Device Type')
plt.ylabel('Order Value')
plt.grid(True, alpha=0.3)
plt.show()
sns.boxplot(data=order_level_1, x='payment_method', y='revenue')
plt.title('AOV Distribution by Payment Method')
plt.xlabel('Payment Method')
plt.ylabel('Order Value')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.show()
top_products = df1.groupby('product_id')['revenue'].sum().nlargest(10).index
product_data = df1[df1['product_id'].isin(top_products)]
product_data.groupby('product_id')['revenue'].sum().plot(kind='bar')
plt.title('Top 10 Products by Revenue')
plt.ylabel('Revenue')
plt.grid(True, alpha=0.3)
plt.show()
summary = order_level_1.groupby('order_source')['revenue'].agg(['count','mean'])
summary.plot(kind='bar')
plt.title('Order Source: Volume vs AOV')
plt.grid(True, alpha=0.3)
plt.show()

sns.histplot(data=order_level_1, x='revenue', bins=30)
plt.title('AOV Distribution')
plt.grid(True, alpha=0.3)
plt.show()

df1['order_date'] = pd.to_datetime(df1['order_date'])
aov_month = df1.groupby(df1['order_date'].dt.to_period('M'))['revenue'].sum() / df1.groupby(df1['order_date'].dt.to_period('M'))['order_id'].nunique()
aov_month.plot(marker='o')
plt.title('AOV Trend Over Month')
plt.grid(True, alpha=0.3)
plt.show()

df1['order_date'] = pd.to_datetime(df1['order_date'])
aov_year = df1.groupby(df1['order_date'].dt.to_period('Y'))['revenue'].sum() / df1.groupby(df1['order_date'].dt.to_period('Y'))['order_id'].nunique()
aov_year.plot(marker='o')
plt.title('AOV Trend Over Year')
plt.grid(True, alpha=0.3)
plt.show()

products=pd.read_csv('data/products.csv')
products = products[products['cogs'] < products['price']]
df2=order_items.merge(products,how='left',on='product_id')
print(df2)

print(df2['order_id'].duplicated().any())
print(df2['product_id'].duplicated().any())
df2['revenue']=df2['unit_price']*df2['quantity']
order_level_2 = df2.groupby(['order_id','category','segment'])['revenue'].sum().reset_index()
order_level_2.groupby('category')['revenue'].agg(['count','mean','median'])
order_level_2.groupby('segment')['revenue'].agg(['count','mean','median'])

sns.boxplot(data=order_level_2, x='category', y='revenue')
plt.title('AOV Distribution by Category')
plt.xlabel('Category')
plt.ylabel('Order Value')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.show()

sns.boxplot(data=order_level_2, x='segment', y='revenue')
plt.title('AOV Distribution by Segment')
plt.xlabel('Segment')
plt.ylabel('Order Value')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.show()

customers=pd.read_csv('data/customers.csv')
df3= df1.merge(customers,how='left',on='customer_id')
order_level_3 = df3.groupby(['order_id','gender','age_group','acquisition_channel','city'])['revenue'].sum().reset_index()
order_level_3.groupby('gender')['revenue'].agg(['count','mean','median'])
order_level_3.groupby('age_group')['revenue'].agg(['count','mean','median'])
order_level_3.groupby('acquisition_channel')['revenue'].agg(['count','mean','median'])
order_level_3.groupby('city')['revenue'].agg(['count','mean','median'])

sns.boxplot(data=order_level_3, x='gender', y='revenue')
plt.title('AOV Distribution by Gender')
plt.xlabel('Gender')
plt.ylabel('Order Value')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.show()

sns.boxplot(data=order_level_3, x='age_group', y='revenue')
plt.title('AOV Distribution by Age group')
plt.xlabel('Age group')
plt.ylabel('Order Value')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.show()

sns.boxplot(data=order_level_3, x='acquisition_channel', y='revenue')
plt.title('AOV Distribution by Acquisition channel')
plt.xlabel('Acquisition channel')
plt.ylabel('Order Value')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.show()

top_city =order_level_3['city'].value_counts().head(5).index
sns.boxplot(data=order_level_3[order_level_3['city'].isin(top_city)], x='city', y='revenue')
plt.title('AOV by Top Cities')
plt.xlabel('City')
plt.ylabel('Order Value')
plt.grid(True, alpha=0.3)
plt.show()

