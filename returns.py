import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

geography=pd.read_csv('data/geography.csv')
customers=pd.read_csv('data/customers.csv')
orders=pd.read_csv('data/orders.csv')
returns=pd.read_csv('data/returns.csv')
returns['return_date'] = pd.to_datetime(returns['return_date'])
returns['return_month'] = returns['return_date'].dt.to_period('M')
products=pd.read_csv('data/products.csv')
df1=returns.merge(products,on='product_id')
print(returns.info())
print(df1)

sns.histplot(returns['refund_amount'], bins=50)

monthly_return = returns.groupby('return_month')['return_quantity'].sum().sort_index()
monthly_return.plot(kind='line', marker='o')
plt.title('Return Quantity Trend by Month')
plt.xlabel('Month')
plt.ylabel('Return Quantity')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

returns['return_reason'].value_counts().plot(kind='bar')
plt.title('Return Reason Count')
plt.show()

reason_trend = pd.crosstab(
    returns['return_month'],
    returns['return_reason']
).sort_index()
reason_trend_pct = reason_trend.div(reason_trend.sum(axis=1), axis=0)
reason_trend_pct.plot(kind='area', stacked=True)
plt.title('Return Reason Share Over Time (%)')
plt.xlabel('Month')
plt.ylabel('Proportion')
plt.xticks(rotation=45)
plt.show()

top_cat = df1['category'].value_counts().head(5).index
category_trend = pd.crosstab(
    df1[df1['category'].isin(top_cat)]['return_month'],
    df1[df1['category'].isin(top_cat)]['category'])
category_trend = category_trend.sort_index()
category_pct = category_trend.div(category_trend.sum(axis=1), axis=0)
category_pct.plot(kind='area', stacked=True)
plt.title('Category return share Over Time')
plt.xlabel('Month')
plt.ylabel('Proportion')
plt.xticks(rotation=45)
plt.show()

top_products = df1['product_name'].value_counts().head(10).index
product_trend = df1[df1['product_name'].isin(top_products)]
product_trend = pd.crosstab(product_trend['return_month'],product_trend['product_name'])
product_trend = product_trend.sort_index()
category_trend.plot(kind='line', marker='o')
plt.title('Product return Trend Over Time')
plt.xlabel('Month')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

size_trend = pd.crosstab(df1['return_month'],df1['size'])
size_trend = size_trend.sort_index()
size_trend_pct = size_trend.div(size_trend.sum(axis=1), axis=0)
size_trend_pct.plot(
    kind='area',
    stacked=True,
    figsize=(12,6),
    alpha=0.8)
plt.title('Size Distribution Over Time')
plt.xlabel('Month')
plt.ylabel('Percentage')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

df2=returns.merge(orders,on='order_id')
device_trend = pd.crosstab(df2['return_month'],df2['device_type'])
device_trend_pct = device_trend.div(device_trend.sum(axis=1), axis=0)
device_trend_pct.plot(figsize=(12,6), marker='o')
plt.title('Device Type Trend Over Time (%)')
plt.xlabel('Month')
plt.ylabel('Percentage')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Device', bbox_to_anchor=(1.05,1))
plt.tight_layout()
plt.show()

device_refund = df2.groupby('device_type')['refund_amount'].mean()
device_refund.plot(kind='bar')
plt.title('Average Refund Amount by Device')
plt.xlabel('Device')
plt.ylabel('Mean Refund Amount')
plt.xticks(rotation=45)
plt.show()

payment_trend = pd.crosstab(df2['return_month'], df2['payment_method']).sort_index()
payment_trend_pct = payment_trend.div(payment_trend.sum(axis=1), axis=0)
payment_trend_pct.plot(
    kind='area',
    stacked=True,
    figsize=(14,6),
    alpha=0.8)
plt.title('Payment Method Share Over Time')
plt.xlabel('Month')
plt.ylabel('Percentage')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

df2['refund_amount'] = pd.to_numeric(df2['refund_amount'], errors='coerce')
df2['payment_method'] = df2['payment_method'].fillna('Unknown')
payment_method_refund = df2.groupby('payment_method')['refund_amount'].agg(['count','mean','sum'])
payment_method_refund.plot(kind='bar', figsize=(10,6))
plt.title('Refund Metrics by Payment Method')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

order_source_trend = pd.crosstab(df2['return_month'], df2['order_source']).sort_index()
source_pct = order_source_trend.div(order_source_trend.sum(axis=1), axis=0)
source_pct.plot(kind='area', stacked=True)
plt.title('Order source Return share Over Time')
plt.xlabel('Month')
plt.ylabel('Proportion')
plt.xticks(rotation=45)
plt.show()

order_source_refund = df2.groupby('order_source')['refund_amount'].agg(['count','mean','sum'])
order_source_refund['count'].plot(kind='bar', title='Number of Returns by Order source')
plt.show()
order_source_refund['sum'].plot(kind='bar', title='Total Refund by Order source')
plt.show()
order_source_refund['mean'].plot(kind='bar', title='Average Refund by Order source')
plt.show()

returns = df2.groupby('order_source')['order_id'].count()
orders = orders.groupby('order_source')['order_id'].count()
return_rate = returns / orders
return_rate.plot(kind='bar')
plt.title('Return Rate by Order Source')
plt.show()

summary = df2.groupby('payment_method').agg(
    orders=('order_id','nunique'),
    returns=('refund_amount','count'),
    total_refund=('refund_amount','sum'))
summary['return_rate'] = summary['returns'] / summary['orders']
summary['refund_per_order'] = summary['total_refund'] / summary['orders']

print(df2.info())
df2=df2.merge(geography,on='zip',how='left')
df3= df2.merge(customers,on='customer_id',how='left')
age_group_return_trend = pd.crosstab(df3['return_month'], df3['age_group']).sort_index()
age_pct = age_group_return_trend.div(age_group_return_trend.sum(axis=1), axis=0)
age_pct.plot(
    kind='area',
    stacked=True,
    figsize=(12,6),
    alpha=0.8)
plt.title('Age Group Return Share Over Time')
plt.xlabel('Month')
plt.ylabel('Percentage')
plt.xticks(rotation=45)
plt.legend(title='Age Group', bbox_to_anchor=(1.05,1))
plt.tight_layout()
plt.show()

order_source_return_trend = pd.crosstab(df3['return_month'], df3['order_source']).sort_index()
source_pct = order_source_return_trend.div(order_source_return_trend.sum(axis=1), axis=0)
source_pct.plot(
    kind='area',
    stacked=True,
    figsize=(12,6),
    alpha=0.8)
plt.title('Order Source Return Share Over Time')
plt.xlabel('Month')
plt.ylabel('Percentage')
plt.xticks(rotation=45)
plt.legend(title='Order Source', bbox_to_anchor=(1.05,1))
plt.tight_layout()
plt.show()

gender_return_trend = pd.crosstab(df3['return_month'], df3['gender']).sort_index()
gender_pct = gender_return_trend.div(gender_return_trend.sum(axis=1), axis=0)
gender_pct.plot(
    kind='area',
    stacked=True,
    figsize=(12,6),
    alpha=0.8)
plt.title('Gender Return Share Over Time')
plt.xlabel('Month')
plt.ylabel('Percentage')
plt.xticks(rotation=45)
plt.legend(title='Gender', bbox_to_anchor=(1.05,1))
plt.tight_layout()
plt.show()

acquisition_channel_return_trend = pd.crosstab(df3['return_month'], df3['acquisition_channel']).sort_index()
acq_pct = acquisition_channel_return_trend.div(
    acquisition_channel_return_trend.sum(axis=1), axis=0)
acq_pct.plot(
    kind='area',
    stacked=True,
    figsize=(12,6),
    alpha=0.8)
plt.title('Acquisition Channel Return Share Over Time')
plt.xlabel('Month')
plt.ylabel('Percentage')
plt.xticks(rotation=45)
plt.legend(title='Channel', bbox_to_anchor=(1.05,1))
plt.tight_layout()
plt.show()

region_return_trend = pd.crosstab(df3['return_month'], df3['region']).sort_index()
region_pct = region_return_trend.div(region_return_trend.sum(axis=1), axis=0)
region_pct.plot(
    kind='area',
    stacked=True,
    figsize=(12,6),
    alpha=0.8)
plt.title('Region Return Share Over Time')
plt.xlabel('Month')
plt.ylabel('Percentage')
plt.xticks(rotation=45)
plt.legend(title='Region', bbox_to_anchor=(1.05,1))
plt.tight_layout()
plt.show()

