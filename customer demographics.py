import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

customers=pd.read_csv('data/customers.csv')
geography=pd.read_csv('data/geography.csv')
payments=pd.read_csv('data/payments.csv')
orders=pd.read_csv('data/orders.csv')
order_items=pd.read_csv('data/order_items.csv')
returns=pd.read_csv('data/returns.csv')

print(payments.columns)
print(payments.head())

df1 = customers.merge(geography, how='left', on='zip') \
    .merge(orders, how='left', on='customer_id') \
    .merge(payments, how='left', on='order_id', suffixes=('', '_pay')) \
    .merge(order_items, how='left', on='order_id', suffixes=('', '_item')) \
    .merge(returns, how='left', on='order_id')

df1['revenue'] = df1['unit_price'] * df1['quantity']
order_level_1 = df1.groupby([
    'order_id']).agg(
 revenue=('revenue', 'sum'),
    age_group=('age_group', 'first')
).reset_index()

print(df1['age_group'].unique())
print(df1['order_status'].unique())

device_dist = pd.crosstab(
    index=df1['age_group'],
    columns=df1['device_type'],
    normalize='index')
device_dist.plot(kind='bar', stacked=True)
plt.title('Device Distribution by Age Group')
plt.ylabel('Percentage')
plt.show()

order_source_dist = pd.crosstab(
    index=df1['age_group'],
    columns=df1['order_source'],
    normalize='index')
order_source_dist.plot(kind='bar', stacked=True)
plt.title('Order source Distribution by Age Group')
plt.ylabel('Percentage')
plt.show()

acquisition_channel_dist = pd.crosstab(
    index=df1['age_group'],
    columns=df1['acquisition_channel'],
    normalize='index')
acquisition_channel_dist.plot(kind='bar', stacked=True)
plt.title('Acquisition channel Distribution by Age Group')
plt.ylabel('Percentage')
plt.show()


payment_method_dist = pd.crosstab(
    index=df1['age_group'],
    columns=df1['payment_method'],
    normalize='index')
payment_method_dist.plot(kind='bar', stacked=True)
plt.title('Payment method Distribution by Age Group')
plt.ylabel('Percentage')
plt.show()

df1['payment_bin'] = pd.cut(df1['payment_value'], bins=[0, 50, 100, 200, 500, 1000],
    labels=['0-50', '50-100', '100-200', '200-500', '500+']
)
payment_value_dist = pd.crosstab(
    index=df1['age_group'],
    columns=df1['payment_bin'],
    normalize='index')
payment_value_dist.plot(kind='bar', stacked=False, figsize=(10,6))
plt.title('Payment Distribution by Age Group')
plt.ylabel('Percentage')
plt.show()

order_count= df1.groupby('age_group')['order_id'].nunique().reset_index()
order_count.plot(kind='bar',x='age_group', y='order_id')
plt.title('Order Count by Age Group')
plt.ylabel('Orders')
plt.show()

installments_dist = pd.crosstab(
    index=df1['age_group'],
    columns=df1['installments'])
installments_dist.plot(kind='bar', stacked=True)
plt.title('Fin Installments by Age Group')
plt.ylabel('Count')
plt.show()

region_dist = pd.crosstab(
    index=df1['age_group'],
    columns=df1['region'],
    normalize='index')
region_dist.plot(kind='bar', stacked=True)
plt.title('Region Distribution by Age Group')
plt.ylabel('Percentage')
plt.show()
aov_age = order_level_1.groupby('age_group', as_index=False)['revenue'].mean()
age_order = ['18-24', '25-34', '35-44', '45-54', '55+']
aov_age['age_group'] = pd.Categorical(aov_age['age_group'], categories=age_order, ordered=True)
aov_age = aov_age.sort_values('age_group')
plt.figure(figsize=(8,5))
plt.bar(aov_age['age_group'], aov_age['revenue'])
plt.title('AOV by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Average Order Value')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

returns_dist = pd.crosstab(
    df1['age_group'],
    df1['return_reason'],
    normalize='index')
returns_dist.plot(kind='bar', stacked=True)
plt.title('Return Reason by Age Group')
plt.ylabel('Percentage')
plt.show()


