import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

reviews=pd.read_csv('data/reviews.csv')
products=pd.read_csv('data/products.csv')
customers=pd.read_csv('data/customers.csv')
df1=reviews.merge(products,how='inner',on='product_id')
pd.set_option('display.max_column',None)
print(df1)

segment_rating = df1.groupby('segment')['rating'].mean().reset_index()
category_rating = df1.groupby('category')['rating'].mean().reset_index()
product_rating = df1.groupby(['product_id','product_name'])['rating'].mean().reset_index()
color_rating = df1.groupby('color')['rating'].mean().reset_index()
size_rating = df1.groupby('size')['rating'].mean().reset_index()

df1['margin']=df1['price']-df1['cogs']
df1['margin_pct']=df1['margin']/df1['price']
df1[['price', 'rating', 'margin_pct']].corr()
sns.heatmap(df1[['price','rating','margin_pct']].corr(), annot=True)
plt.title('Correlation Matrix')
plt.show()

df2=reviews.merge(customers,how='inner',on='customer_id')
pd.set_option('display.max_column',None)

customer_seg_rating=df2.groupby('age_group')['rating'].mean().reset_index()
customer_seg_rating.plot(kind='bar', x='age_group', y='rating')
plt.title('Average Rating by Age Group')
plt.ylabel('Average Rating')
plt.xlabel('Age Group')
plt.xticks(rotation=0)
plt.show()

sns.boxplot(data=df2, x='age_group', y='rating')
plt.title(' Rating by Age Group')
plt.ylabel('Rating')
plt.xlabel('Age Group')
plt.xticks(rotation=0)
plt.show()

df2['review_date'] = pd.to_datetime(df2['review_date'])
time_trend = df2.groupby(df2['review_date'].dt.to_period('M')).agg(
    avg_rating=('rating', 'mean'),
    total_orders=('order_id', 'nunique'))
time_trend.index = time_trend.index.to_timestamp()
plt.figure(figsize=(12,6))
plt.plot(time_trend.index, time_trend['avg_rating'], marker='o', linewidth=2)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.title('Average Rating Over Time', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Average Rating')
plt.ylim(3, 5)
plt.tight_layout()
plt.show()

sns.barplot(data=category_rating, x='category', y='rating')
plt.xticks(rotation=45)
plt.title('Average Rating by Category')
plt.show()

sns.barplot(data=segment_rating, x='segment', y='rating')
plt.title('Average Rating by Segment')
plt.show()
