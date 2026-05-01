import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

shipments=pd.read_csv('data/shipments.csv')
order_items=pd.read_csv('data/order_items.csv')
orders=pd.read_csv('data/orders.csv')
geography=pd.read_csv('data/geography.csv')

shipments['ship_date'] = pd.to_datetime(shipments['ship_date'])
shipments['delivery_date'] = pd.to_datetime(shipments['delivery_date'])
shipments['shipping_time'] = (shipments['delivery_date'] - shipments['ship_date']).dt.days
shipments['year_month'] = shipments['ship_date'].dt.to_period('M')
shipping_trend =shipments.groupby('year_month')['shipping_time'].mean()
shipping_trend = shipping_trend.sort_index()
shipping_trend.index = shipping_trend.index.to_timestamp()
rolling_mean = shipping_trend.rolling(3).mean()
plt.figure(figsize=(12,6))
plt.plot(shipping_trend, alpha=0.3, label='Raw Mean')
plt.plot(rolling_mean, linewidth=2.5, label='3-Month Rolling Avg')
plt.title('Smoothed Shipping Time Trend')
plt.xlabel('Month')
plt.ylabel('Days')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.show()

sns.regplot(data=shipments, x='shipping_fee', y='shipping_time')

order_items['revenue']=order_items['unit_price']*order_items['quantity']
order_items['order_level_1'] = order_items.groupby('order_id')['revenue'].transform('sum')
shipments['shipping_fee'].describe()

filtered=shipments[shipments['shipping_fee'] < shipments['shipping_fee'].quantile(0.99)]
sns.histplot(filtered['shipping_fee'], bins=40, kde=True)
plt.title('Distribution of Shipping Fee')
plt.xlabel('Shipping Fee')
plt.ylabel('Frequency')
plt.show()

order_level = order_items.groupby('order_id', as_index=False)['revenue'].sum()
order_level.rename(columns={'revenue': 'order_level_1'}, inplace=True)
df1=shipments.merge(order_items,on='order_id')
df_plot = df1[
    (df1['order_level_1'] > 0) &
    (df1['shipping_fee'] > 0)]
plt.figure(figsize=(10,6))
plt.hexbin(
    df1['order_level_1'],
    df1['shipping_fee'],
    gridsize=40,
    cmap='Blues',
    mincnt=5)
plt.xscale('log')
plt.yscale('log')
plt.colorbar(label='Count')
plt.xlabel('Revenue per Order (log)')
plt.ylabel('Shipping Fee')
plt.title('Rev per order vs shipping fee')
plt.tight_layout()
plt.show()

df2=shipments.merge(orders,on='order_id')\
    .merge(geography,on='zip')
df2= df2[~df2['order_status'].isin(['paid', 'cancelled','created'])]
top_city = df2['city'].value_counts().head(10).index
df_city=df2[df2['city'].isin(top_city)]
order = (
    df_city.groupby('city')['shipping_time']
    .median()
    .sort_values()
    .index)
sns.boxplot(
    data=df_city,
    x='city',
    y='shipping_time',
    order=order,
    showfliers=False)
plt.title('Shipping Time by City (Sorted)')
plt.xticks(rotation=45)
plt.show()

order_fee = (
    df_city.groupby('city')['shipping_fee']
    .median()
    .sort_values()
    .index)
sns.boxplot(
    data=df_city,
    x='city',
    y='shipping_fee',
    order=order_fee,
    showfliers=False)
plt.title('Shipping Fee by City (Sorted)')
plt.xticks(rotation=45)
plt.show()

sns.boxplot(data=df2, x='order_status', y='shipping_time',showfliers=False)
plt.xticks(rotation=45)
plt.title('Shipping Time by Order Status')
plt.show()

df2 = df2[df2['shipping_time'] > 0]
df2['fee_per_day'] = df2['shipping_fee'] / df2['shipping_time']
df_plot = df2[
    df2['fee_per_day'] < df2['fee_per_day'].quantile(0.95)]
df_city = df_plot[df_plot['city'].isin(top_city)]
order_eff = (
    df_city.groupby('city')['fee_per_day']
    .median()
    .sort_values()
    .index)
sns.boxplot(
    data=df_city,
    x='city',
    y='fee_per_day',
    order=order_eff,
    showfliers=False)
plt.title('Shipping Cost Efficiency by City (Sorted, Cleaned)')
plt.xticks(rotation=45)
plt.ylabel('Fee per Day')
plt.show()

df_plot = df2[
    df2['shipping_fee'] < df2['shipping_fee'].quantile(0.95)]
sns.boxplot(data=df_plot, x='shipping_time', y='shipping_fee',showfliers=False)
plt.title('Shipping Time vs Fee')
plt.show()

sns.violinplot(
    data=df2,
    x='shipping_time',
    y='shipping_fee',
    inner='quartile',
    cut=0)
plt.title('Shipping Fee Distribution by Shipping Time')
plt.show()











