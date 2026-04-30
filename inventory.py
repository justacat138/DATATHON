import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

inventory=pd.read_csv('data/inventory.csv')
print(inventory.columns)
print(inventory)
inventory['snapshot_date']=pd.to_datetime(inventory['snapshot_date'])
inventory = inventory.sort_values(['snapshot_date'])
print(inventory)

inventory['year']=inventory['snapshot_date'].dt.year

df = inventory.groupby('snapshot_date')['stock_on_hand'].sum().reset_index()
plt.figure(figsize=(12,6))
plt.plot(df['snapshot_date'], df['stock_on_hand'])
plt.title('Total Stock Over Time')
plt.show()


yearly = inventory.groupby('year').agg({
    'units_sold': 'sum',
    'units_received': 'sum'
}).reset_index()
yearly =yearly.sort_values('year')
plt.figure(figsize=(12,6))
plt.plot(yearly['year'], yearly['units_sold'], label='Units Sold')
plt.plot(yearly['year'], yearly['units_received'], label='Units Received')
plt.title('Units Sold vs Units Received Over Time-Year')
plt.xlabel('Date')
plt.ylabel('Units')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

df1 = inventory.groupby('snapshot_date')['units_received'].sum().reset_index()
plt.figure(figsize=(12,6))
plt.plot(df1['snapshot_date'], df1['units_received'])
plt.title('Units Received Over Time')
plt.xticks(rotation=45)
plt.show()

df2 = inventory.groupby('snapshot_date')['units_sold'].sum().reset_index()
plt.figure(figsize=(12,6))
plt.plot(df2['snapshot_date'], df2['units_sold'])
plt.title('Units Sold Over Time')
plt.xticks(rotation=45)
plt.show()

monthly = inventory.groupby('snapshot_date').agg({
    'days_of_supply': 'mean',
    'units_sold': 'sum'
}).reset_index()
monthly = monthly.sort_values('snapshot_date')
plt.figure(figsize=(12,6))
plt.plot(monthly['snapshot_date'], monthly['days_of_supply'], label='Days of Supply')
plt.plot(monthly['snapshot_date'], monthly['units_sold'], label='Units Sold')
plt.title('Days of Supply vs Units Sold Over Time')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

inventory['fill_rate_bin'] = pd.cut(inventory['fill_rate'], bins=10)
df3 = inventory.groupby('fill_rate_bin',observed=True)['units_sold'].mean().reset_index()
plt.figure(figsize=(10,6))
plt.bar(df3['fill_rate_bin'].astype(str), df3['units_sold'])
plt.xlabel('Fill Rate')
plt.ylabel('Units Sold')
plt.title('Fill Rate vs Units Sold')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

inventory['estimated_demand'] = np.where(
    inventory['fill_rate'] > 0.1,
    inventory['units_sold'] / inventory['fill_rate'],
    np.nan)
plt.figure(figsize=(8,6))
plt.scatter(inventory['estimated_demand'], inventory['units_sold'])
plt.xscale('log')
plt.xlabel('Estimated Demand')
plt.ylabel('Units Sold')
plt.title('Estimated Demand vs Units Sold')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,6))
plt.hist(inventory['sell_through_rate'], bins=20)
plt.xlabel('Sell-through Rate')
plt.ylabel('Frequency')
plt.title('Distribution of Sell-through Rate')
plt.tight_layout()
plt.show()

agg = inventory.groupby('product_id').agg({
    'days_of_supply': 'mean',
    'sell_through_rate': 'mean'
}).reset_index()
plt.figure(figsize=(8,6))
plt.scatter(agg['days_of_supply'], agg['sell_through_rate'])
# đường trung bình
plt.axvline(agg['days_of_supply'].mean(), linestyle='--')
plt.axhline(agg['sell_through_rate'].mean(), linestyle='--')
plt.xlabel('Days of Supply')
plt.ylabel('Sell-through Rate')
plt.title('Sell-through vs Days of Supply (Quadrant)')
plt.show()

monthly = inventory.groupby('snapshot_date')['stockout_days'].sum().reset_index()
monthly['rolling_avg'] = monthly['stockout_days'].rolling(window=3).mean()
plt.figure(figsize=(12, 6))
plt.plot(monthly['snapshot_date'], monthly['stockout_days'], label='Tổng theo tháng', alpha=0.5)
plt.plot(monthly['snapshot_date'], monthly['rolling_avg'], label='Xu hướng 3 tháng', color='red', linewidth=2)
plt.title('Phân tích xu hướng ngày hết hàng', fontsize=14)
plt.xlabel('Ngày')
plt.ylabel('Tổng số ngày hết hàng')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

stockout_rate = inventory['stockout_flag'].value_counts(normalize=True)
plt.figure(figsize=(8, 6))
bars = plt.bar(stockout_rate.index.astype(str), stockout_rate.values, color=['#d9534f', '#5cb85c']) # Đỏ cho hết hàng, xanh cho còn hàng
# Thêm con số phần trăm trên đầu mỗi cột
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, f'{yval*100:.1f}%', ha='center', va='bottom', fontweight='bold')
plt.title('Tỷ lệ Hết hàng (Stockout Rate)', fontsize=14)
plt.ylabel('Tỷ lệ (%)')
# Đổi nhãn trục X cho rõ nghĩa hơn thay vì chỉ để 0 và 1
plt.xticks(['1', '0'], ['Hết hàng (1)', 'Còn hàng (0)'])
plt.show()

# Đổi tên các index và columns để hiển thị đẹp hơn
cross_named = pd.crosstab(inventory['reorder_flag'], inventory['stockout_flag'])
cross_named = cross_named.rename(
    index={0: 'Chưa đặt hàng', 1: 'Đã đặt hàng'},
    columns={0: 'Còn hàng', 1: 'Hết hàng'})

# Vẽ biểu đồ tỷ lệ phần trăm (Normalized stacked bar)
cross_pct = cross_named.div(cross_named.sum(1), axis=0)
cross_pct.plot(kind='bar', stacked=True, figsize=(10, 6), color=['#5cb85c', '#d9534f'])
plt.title('Mối quan hệ giữa Đặt hàng lại và Hết hàng (%)', fontsize=14)
plt.xlabel('Trạng thái đặt hàng')
plt.ylabel('Tỷ lệ phần trăm')
plt.legend(title='Trạng thái kho', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
# Thêm nhãn % vào giữa các thanh
for n, x in enumerate([*cross_pct.index.values]):
    for (proportion, y_loc) in zip(cross_pct.loc[x],
                                   cross_pct.loc[x].cumsum()):
        plt.text(x=n,
                 y=(y_loc - proportion / 2),
                 s=f'{np.round(proportion * 100, 1)}%',
                 color="white", fontsize=12, fontweight='bold', ha="center")
plt.tight_layout()
plt.show()


seg_sales = inventory.groupby('segment')['units_sold'].sum().reset_index()
plt.figure(figsize=(10, 6))
# Vẽ cột ngang bằng plt.barh
plt.barh(seg_sales['segment'], seg_sales['units_sold'], color='teal')
plt.xlabel('Số lượng đơn vị bán ra')
plt.title('Phân tích Sản lượng theo Phân khúc')
plt.gca().invert_yaxis() # Đảo ngược để nhóm cao nhất nằm ở trên cùng
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.show()

# Sắp xếp giảm dần
seg = inventory.groupby('segment')['units_sold'].sum().reset_index()
seg = seg.sort_values(by='units_sold', ascending=False)
seg['total'] = seg['units_sold'].sum()
seg['percentage'] = seg['units_sold'] / seg['total'] * 100
seg['cumulative_pct'] = seg['percentage'].cumsum()
fig, ax1 = plt.subplots(figsize=(10,6))
# Vẽ biểu đồ cột
ax1.bar(seg['segment'], seg['percentage'], color='C0')
ax1.set_ylabel('Đóng góp doanh thu (%)', color='C0')
# Vẽ đường tích lũy
ax2 = ax1.twinx()
ax2.plot(seg['segment'], seg['cumulative_pct'], color='C1', marker='D', ms=5)
ax2.axhline(80, color='red', linestyle='--', alpha=0.5) # Đường ngưỡng 80%
ax2.set_ylabel('Tỷ lệ tích lũy (%)', color='C1')
plt.title('Phân tích Doanh thu theo Phân khúc')
plt.show()

seg_str = inventory.groupby('segment')['sell_through_rate'].mean().reset_index()
plt.figure(figsize=(10, 6))
# Nhân với 100 để chuyển sang %
bars = plt.bar(seg_str['segment'], seg_str['sell_through_rate'] * 100, color='mediumpurple')
# Thêm nhãn % lên đầu cột
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, f'{yval:.1f}%', ha='center', fontweight='bold')
plt.title('Tỷ lệ Bán hết (STR) theo Phân khúc', fontsize=14)
plt.ylabel('Tỷ lệ phần trăm (%)')
plt.xticks(rotation=45)
plt.ylim(0, max(seg_str['sell_through_rate'] * 100) + 5)
plt.tight_layout()
plt.show()

seg_dos = inventory.groupby('segment')['days_of_supply'].mean().reset_index()
# Sắp xếp giảm dần để dễ so sánh
seg_dos = seg_dos.sort_values('days_of_supply', ascending=False)
plt.figure(figsize=(12, 6))
bars = plt.bar(seg_dos['segment'], seg_dos['days_of_supply'], color='salmon')
# Thêm đường ngưỡng mục tiêu (ví dụ 90 ngày) để thấy sự chênh lệch
plt.axhline(y=90, color='red', linestyle='--', label='Ngưỡng mục tiêu (90 ngày)')
# Thêm nhãn số trên đầu cột
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 10,
             f'{int(height)}', ha='center', fontweight='bold')
plt.title('Số ngày dự trữ (DOS) trung bình theo Phân khúc', fontsize=14)
plt.ylabel('Số ngày')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

seg = inventory.groupby('segment').agg({
    'units_sold': 'sum',
    'units_received': 'sum'
}).reset_index()
# Thiết lập vị trí các cột
x = np.arange(len(seg))
width = 0.35  # Độ rộng mỗi cột
fig, ax = plt.subplots(figsize=(12, 6))
rects1 = ax.bar(x - width/2, seg['units_sold'], width, label='Đã bán (Sold)', color='#1f77b4')
rects2 = ax.bar(x + width/2, seg['units_received'], width, label='Nhận về (Received)', color='#ff7f0e')
# Thêm nhãn, tiêu đề và định dạng
ax.set_ylabel('Số lượng đơn vị')
ax.set_title('So sánh Cung (Received) và Cầu (Sold) theo Phân khúc', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(seg['segment'], rotation=45)
ax.legend()
# Thêm lưới ngang để dễ so sánh
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 7))
for seg in inventory['segment'].unique():
    subset = inventory[inventory['segment'] == seg]
    subset = subset[subset['days_of_supply'] > 0]
    plt.scatter(subset['days_of_supply'], subset['sell_through_rate'], label=seg, alpha=0.5, s=20)
# Sử dụng thang Log cho trục X
plt.xscale('log')
plt.xlabel('Days of Supply (Log Scale)')
plt.ylabel('Sell-through Rate')
plt.title('Hiệu suất Phân khúc (Thang Log giúp nhìn rõ vùng DOS thấp)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.tight_layout()
plt.show()

top = inventory.groupby('product_name')['units_sold'].sum().reset_index()
top = top.sort_values('units_sold', ascending=False).head(10)
plt.figure(figsize=(10,5))
plt.barh(top['product_name'], top['units_sold'])
plt.title('Top 10 Products by Units Sold')
plt.xlabel('Units Sold')
plt.gca().invert_yaxis()
plt.show()

bottom = inventory.groupby('product_name')['units_sold'].sum().reset_index()
bottom = bottom.sort_values('units_sold', ascending=True).head(10)
plt.figure(figsize=(10,5))
plt.barh(bottom['product_name'], bottom['units_sold'])
plt.xlabel('Units Sold')
plt.ylabel('Product Name')
plt.title('Bottom 10 Products by Units Sold')
# đảo chiều để product bán kém nhất nằm trên cùng
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Đầu tiên, gộp thêm cột Segment vào bảng agg của bạn
agg_with_segment = inventory.groupby(['product_name', 'segment']).agg({
    'units_sold': 'sum',
    'sell_through_rate': 'mean'
}).reset_index()
plt.figure(figsize=(12, 7))
sns.scatterplot(data=agg_with_segment,
                x='units_sold',
                y='sell_through_rate',
                hue='segment', # Phân bổ màu theo nhóm
                alpha=0.6,
                s=60)
plt.title('Hiệu suất Sản phẩm theo từng Phân khúc')
plt.xlabel('Tổng sản lượng bán ra')
plt.ylabel('Tỷ lệ bán hết (STR) trung bình')
plt.legend(title='Phân khúc', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

plt.figure(figsize=(10,6))
sns.boxplot(x='segment', y='units_sold', data=inventory)
plt.xlabel('Segment')
plt.ylabel('Units Sold')
plt.title('Distribution of Units Sold by Segment')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()