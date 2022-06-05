from data_process import df
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ----------淘宝在售手机价格区间统计---------
plt.rcParams['font.family']=['Arial Unicode MS']
plt.figure(figsize=(10,5),dpi=200)

#发现手机原价数据有异常，进行清洗
df=df.drop(df[df['商品原价']>10000].index)

x=df['价格等级']
y=df.groupby('价格等级').count().reset_index

plt.hist(x,bins=12,color='green',align='mid')
plt.title('淘宝在售手机价格区间统计')
plt.xlabel('价格区间')
plt.ylabel('淘宝在售手机数')

plt.savefig('淘宝在售手机价格区间统计')
plt.show()


#-----------商品现价&原价对比------------
#先筛选评分 >4.5的具有分析意义的手机商品
df1=df[df['评分']>4.5]

price1=df1.groupby('品牌')['商品原价'].mean().reset_index()
labels=price1['品牌']

price1=price1['商品原价'].astype(int)
price2=df1.groupby('品牌')['商品现价'].mean().reset_index()
price2=price2['商品现价'].astype(int)

x = np.arange(len(labels))
width = 0.4

fig, ax = plt.subplots(figsize=(40,20))
rects1 = ax.bar(x - width/2, price1, width, label='商品原价')
rects2 = ax.bar(x + width/2, price2, width, label='商品现价')
ax.set_ylabel('价格',fontsize=30)
ax.set_title('手机现价及原价对比',fontsize=50)
ax.set_xticks(x)
plt.xticks(rotation=90)
ax.set_xticklabels(labels)
ax.legend(fontsize=30)

#数据标签设置
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',fontsize=20)


autolabel(rects1)
autolabel(rects2)

plt.tick_params(labelsize=30)
labels = ax.get_xticklabels() + ax.get_yticklabels()

fig.tight_layout()

plt.savefig('手机销售现价&原价对比')
plt.show()

# -------------------手机类型分布词云图---------------------
from wordcloud import WordCloud
from imageio import imread
plt.rcParams['font.family']=['Arial Unicode MS']

df=df[df['手机类型'].notnull()]
df['手机类型']=[i.replace('不祥','不详') for i in df['手机类型']]
df['手机类型']=[i.replace('不详4','不详') for i in df['手机类型']]
df['手机类型']=[i.replace('老年机','老人手机') for i in df['手机类型']]
df['手机类型']=[i.replace('老年手机','老人手机') for i in df['手机类型']]
df['手机类型']=[i.replace('功能机','功能手机') for i in df['手机类型']]
df['手机类型']=[i.replace('老人机','老人手机') for i in df['手机类型']]
df['手机类型']=[i.replace('4G+手机','4G手机') for i in df['手机类型']]
get_type=[i.split('\xa0') for i in df['手机类型'].tolist()]
phone_type=[]
for i in get_type:
    phone_type+=i
word_count=pd.Series(phone_type).value_counts()
font='/Users/zhaosiqi/Library/Fonts/simhei.ttf'
wc = WordCloud(max_words=100,
               scale=12,
               max_font_size=200,
               random_state=30,
               background_color='white',
               font_path=font)

wc2 = wc.fit_words(word_count)

plt.figure(figsize=(15,10))
plt.imshow(wc2)
plt.axis("off")
plt.show()
wc.to_file("手机类型词云图.png")

