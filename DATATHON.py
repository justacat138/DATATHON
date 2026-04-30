import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
customers=pd.read_csv('data/customers.csv')
print(customers['acquisition_channel'].unique())

orders=pd.read_csv('data/orders.csv')
print(orders['order_source'].unique())

web_traffic=pd.read_csv('data/web_traffic.csv')
print(web_traffic.groupby('date')['traffic_source'].nunique())

returns=pd.read_csv('data/returns.csv')
print(returns['return_reason'].unique())

order_items=pd.read_csv('data/order_items.csv')


orders['order_date'] = pd.to_datetime(orders['order_date'])
orders = orders.sort_values(by=['customer_id','order_date'])
orders['inter_order']=orders.groupby('customer_id')['order_date'].diff()
orders['inter_order_gap_days']=orders['inter_order'].dt.days
gaps2=orders['inter_order_gap_days'].dropna()
median_gap=gaps2.median()
print(median_gap)

products=pd.read_csv('data/products.csv')
print(products[['price', 'cogs']].dtypes)
segment_price=products.groupby('segment')['price'].sum()
segment_cogs=products.groupby('segment')['cogs'].sum()
segment_profit=segment_price-segment_cogs
print(segment_profit.idxmax())

df3=returns.merge(products,on='product_id')
result=df3[df3['category']=='Streetwear']['return_reason'].value_counts().idxmax()
print(result)

avg_bounce=web_traffic.groupby('traffic_source')['bounce_rate'].mean()
lowest_source=avg_bounce.idxmin()
print(lowest_source)

promo_percent=order_items['promo_id'].notna().mean()*100
print(promo_percent)

customers=pd.read_csv('data/customers.csv')
df6_=customers.merge(orders,on='customer_id')
df6_1=df6_.merge(order_items,on='order_id')
new_df6_1=df6_1[df6_1['age_group'].notna()]
result=new_df6_1.groupby('age_group')['quantity'].mean()
final_result=result.idxmax()
print(final_result)

result8=orders[orders['order_status']=='cancelled']['payment_method'].value_counts().idxmax()
print(result8)

df9=order_items.merge(products,on='product_id')\
    .merge(returns,on='order_id',how='left')
df9['is_return']=df9['return_id'].notna()
r9=df9.groupby('size')['is_return'].mean().idxmax()
print(r9)

geography=pd.read_csv('data/geography.csv')
payments=pd.read_csv('data/payments.csv')
r10=payments.groupby('installments')['payment_value'].mean().idxmax()
print(r10)

order_items['rev']=order_items['quantity']*order_items['unit_price']
df7_1=order_items.merge(orders,on='order_id',how='left')
df7_2=df7_1.merge(geography,on='zip',how='left')
r7= df7_2.groupby('region')['rev'].sum().idxmax()
print(r7)

print(order_items[order_items['order_id'].duplicated(keep=False)])

print(orders['order_status'].unique())