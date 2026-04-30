import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

promotions=pd.read_csv('data/promotions.csv')
order_items=pd.read_csv('data/order_items.csv')
pd.set_option('display.max_column',None)
print(order_items['promo_id'].unique())
print(order_items['promo_id_2'].unique())
print(promotions['promo_name'].unique())
promotions['start_date'] = pd.to_datetime(promotions['start_date'])
promotions['end_date'] = pd.to_datetime(promotions['end_date'])
promotions['duration_days'] = (promotions['end_date'] - promotions['start_date']).dt.days
promo_duration = promotions.groupby('promo_name')['duration_days'].mean()
promo_duration = promo_duration.sort_values(ascending=False).head(15)
plt.figure(figsize=(12,6))
plt.bar(promo_duration.index, promo_duration.values)
plt.xticks(rotation=30, ha='right')
plt.title('Promotion Duration by Promo Name', fontsize=14, fontweight='bold')
plt.ylabel('Days')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

channel_dist = promotions['promo_channel'].value_counts(normalize=True)
plt.figure(figsize=(6,4))
plt.bar(channel_dist.index, channel_dist.values)
plt.title('Overall Promotion Channel Distribution', fontsize=14, fontweight='bold')
plt.ylabel('Percentage')
plt.xlabel('Channel')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()

discount_dist = promotions['discount_value'].value_counts(normalize=True).sort_index()
plt.figure(figsize=(8,5))
plt.bar(discount_dist.index.astype(str), discount_dist.values)
plt.title('Overall Discount Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Discount Value')
plt.ylabel('Percentage')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

df1 = order_items.merge(promotions, on='promo_id', how='left')
df1['revenue'] = df1['unit_price'] * df1['quantity']
discount_perf = df1.groupby('discount_value')['revenue'].agg(['count','mean'])
fig, ax1 = plt.subplots(figsize=(10,6))
ax1.bar(discount_perf.index.astype(str), discount_perf['count'], alpha=0.7)
ax1.set_ylabel('Number of Orders')

# AOV
ax2 = ax1.twinx()
ax2.plot(discount_perf.index.astype(str), discount_perf['mean'], marker='o', linewidth=2)
ax2.set_ylabel('Average Order Value')

plt.title('Discount Performance: Volume vs AOV', fontsize=14, fontweight='bold')
plt.xlabel('Discount Value')
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()

promotions['start_date'] = pd.to_datetime(promotions['start_date'])
promo_time = promotions.groupby(
    promotions['start_date'].dt.to_period('M')).size()
promo_time.index = promo_time.index.to_timestamp()
plt.figure(figsize=(12,6))
plt.plot(promo_time.index, promo_time.values, alpha=0.4, label='Raw')
plt.plot(promo_time.index, promo_time.values, linewidth=3, label='3M Rolling')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.title('Promotion Trend Over Time')
plt.show()

promo_main = promotions.rename(columns=lambda x: f"{x}_main")
promo_sub = promotions.rename(columns=lambda x: f"{x}_sub")
df1 = order_items.merge(
    promotions.add_suffix('_main'),
    left_on='promo_id',
    right_on='promo_id_main',
    how='left'
)
df1 = df1.merge(
    promotions.add_suffix('_sub'),
    left_on='promo_id_2',
    right_on='promo_id_sub',
    how='left')
df1['revenue'] = df1['unit_price'] * df1['quantity']
df1['promo_name_main'] = df1['promo_name_main'].fillna('')
df1['promo_name_sub'] = df1['promo_name_sub'].fillna('')

df1['final_promo'] = (
    df1['promo_name_main'] + ' + ' + df1['promo_name_sub']
).str.strip()
# remove các case kiểu " + ", "+ A", "A +"
df1['final_promo'] = df1['final_promo'].str.replace(r'^\s*\+\s*|\s*\+\s*$', '', regex=True)
df1.loc[df1['final_promo'] == '', 'final_promo'] = 'No Promo'
# 4. Order-level revenue (AOV đúng nghĩa)
order_level = df1.groupby(['order_id', 'final_promo'], as_index=False)['revenue'].sum()
# 5. Lấy top promo theo số lượng order (KHÔNG phải count dòng)
top_promo = (
    order_level['final_promo']
    .value_counts()
    .head(10)
    .index)
filtered = order_level[order_level['final_promo'].isin(top_promo)]
# 6. Sort theo median AOV
order = (
    filtered.groupby('final_promo')['revenue']
    .median()
    .sort_values()
    .index)
# 7. Plot
plt.figure(figsize=(12,6))
sns.boxplot(
    data=filtered,
    x='final_promo',
    y='revenue',
    order=order)
plt.xticks(rotation=30, ha='right')
plt.title('AOV Distribution by Top Promotions', fontsize=14, fontweight='bold')
plt.xlabel('')
plt.ylabel('Order Value')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

summary = order_level.groupby('final_promo')['revenue'].agg(['count','mean'])
summary = summary.sort_values('count', ascending=False).head(10)
fig, ax1 = plt.subplots(figsize=(14,7))
# Volume
ax1.bar(summary.index, summary['count'], alpha=0.7)
ax1.set_ylabel('Number of Orders',fontsize=12)
# AOV
ax2 = ax1.twinx()
ax2.plot(summary.index, summary['mean'], marker='o', linewidth=2)
ax2.set_ylabel('Average Order Value',fontsize=12)

import textwrap
labels = ['\n'.join(textwrap.wrap(label, 15)) for label in summary.index]
ax1.set_xticks(range(len(labels)))
ax1.set_xticklabels(labels, fontsize=10)

plt.title('Top Promotions: Volume vs AOV', fontsize=16, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()







