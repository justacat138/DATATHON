import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sales = pd.read_csv('data/sales.csv')
print(sales)
sales['Profit'] = sales['Revenue'] - sales['COGS']
sales['Date'] = pd.to_datetime(sales['Date'])
margin_monthly = sales.groupby(sales['Date'].dt.to_period('M')).apply(
    lambda x: x['Profit'].sum() / x['Revenue'].sum())
sales['Date'] = pd.to_datetime(sales['Date'])
monthly =sales.groupby(sales['Date'].dt.to_period('M'))['Revenue'].sum()
monthly.plot()
monthly.plot(title='Revenue Trend')
plt.grid(True, alpha=0.3)
plt.show()

profit_monthly = sales.groupby(sales['Date'].dt.to_period('M'))['Profit'].sum()
profit_monthly.plot()
profit_monthly.plot(title='Profit Trend')
plt.grid(True, alpha=0.3)
plt.show()

margin_monthly.plot()
margin_monthly.plot(title='Margin Trend')
plt.grid(True, alpha=0.3)
plt.show()

sales.groupby(sales['Date'].dt.to_period('M'))['COGS'].sum().plot()

sales[sales['Profit'] < 0].value_counts()

growth = monthly.pct_change()
growth.plot(marker='o', title='Revenue Growth Rate')
plt.axhline(0, color='red', linestyle='--')
plt.grid(True, alpha=0.3)
plt.show()

margin_monthly.plot(title='Profit Margin Trend')
plt.axhline(margin_monthly.mean(), linestyle='--')
plt.show()

fig, ax1 = plt.subplots()
ax1.plot(monthly.index.to_timestamp(), monthly, label='Revenue')
ax1.plot(profit_monthly.index.to_timestamp(), profit_monthly, label='Profit')
plt.legend()
plt.title('Revenue vs Profit Trend')
plt.show()