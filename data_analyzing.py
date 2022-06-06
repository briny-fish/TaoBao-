from data_process import df
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams['font.sans-serif'] = ['SimHei']   #解决中文显示问题
plt.rcParams['axes.unicode_minus'] = False    # 解决中文显示问题

# ----------淘宝在售手机价格区间统计---------
# plt.rcParams['font.family']=['Arial Unicode MS']
plt.figure(figsize=(10,5),dpi=200)

#发现手机原价数据有异常，进行清洗
df1=df.drop(df[df['商品原价']>15000].index)

x=df1['价格等级']
# y = df1.groupby('价格等级').count().reset_index()
x = x.sort_values(ascending=[True])
# y = y.sort_values(by=['价格等级'],ascending=[False])
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
# plt.rcParams['font.family']=['Arial Unicode MS']

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

# ----------------绘制手机品牌词云图--------------
word_count=pd.Series(df['品牌'].tolist()).value_counts()
font='/Users/zhaosiqi/Library/Fonts/simhei.ttf'
# back_pic=imread('pic.jpg')
wc = WordCloud(max_words=100,
               scale=12,
               max_font_size=50,
               random_state=30,
               background_color='white',
               font_path=font)

wc2 = wc.fit_words(word_count)

plt.figure(figsize=(15,10))
plt.imshow(wc2)
plt.axis("off")
plt.show()
wc.to_file("手机品牌词云图.png")

#-----------手机累计销量Top30------------
#先筛选评分 >4.5的具有分析意义的手机商品
from matplotlib.pyplot import MultipleLocator
# plt.rcParams['font.sans-serif'] = ['SimHei']   #解决中文显示问题
# plt.rcParams['axes.unicode_minus'] = False    # 解决中文显示问题
df1=df[df['评分']>4.5]

price1=df1.groupby('品牌')['累计评价数'].sum().reset_index()
price1 = price1.sort_values(by=['累计评价数'],ascending=[False])[:30]
labels=price1['品牌']

price1=price1['累计评价数'].astype(int)

x = np.arange(len(labels))
width = 0.5

fig, ax = plt.subplots(figsize=(40,20))
rects1 = ax.bar(x, price1/10000, width, label='累计销量/百万')
ax.set_ylabel('销量',fontsize=40)
ax.set_title('手机品牌总销量Top30',fontsize=50)
ax.set_xticks(x)
plt.xticks(rotation=90)
ax.set_xticklabels(labels)
ax.legend(fontsize=30)

#数据标签设置
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(str(height)[:4]),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',fontsize=20)


autolabel(rects1)
# autolabel(rects2)

plt.tick_params(labelsize=30)
labels = ax.get_xticklabels() + ax.get_yticklabels()

fig.tight_layout()

plt.savefig('手机总销量Top30')
plt.show()


#--------------不同价格区间手机总销量-------------------
import matplotlib.pyplot as plt                #导入绘图包

# plt.rcParams['font.sans-serif'] = ['SimHei']   #解决中文显示问题
# plt.rcParams['axes.unicode_minus'] = False    # 解决中文显示问题
df1=df[df['评分']>4.5]
result = df1.groupby('价格等级')['累计评价数'].sum().reset_index()          #按年总计股票成交笔数
plt.pie(result['累计评价数'], labels=result['价格等级'],autopct='%3.1f%%')  #以时间为标签，总计成交笔数为数据绘制饼图，并显示3位整数一位小数
plt.title('不同价格区间总销量')
plt.savefig('不同价格区间总销量')#加标题
plt.show()

#--------------不同价格区间手机总销售额-------------------

import matplotlib.pyplot as plt                #导入绘图包

# plt.rcParams['font.sans-serif'] = ['SimHei']   #解决中文显示问题
# plt.rcParams['axes.unicode_minus'] = False    # 解决中文显示问题
df1=df[df['评分']>4.5]
print(df1)
df1['销售额'] = df1.apply(lambda x:x.累计评价数 * x.商品现价,axis = 1)
result = df1.groupby('价格等级')['销售额'].sum().reset_index()          #按年总计股票成交笔数
plt.pie(result['销售额'], labels=result['价格等级'],autopct='%3.1f%%')  #以时间为标签，总计成交笔数为数据绘制饼图，并显示3位整数一位小数
plt.title('不同价格区间总销售额')
plt.savefig('不同价格区间总销售额')#加标题
plt.show()

#-----------------------总销量Top10手机品牌价格构成------------------------------
N = 10
df1=df[df['评分']>4.5]
df0=df[df['评分']>4.5]
price1=df0.groupby('品牌')['累计评价数'].sum().reset_index()
price1 = price1.sort_values(by=['累计评价数'],ascending=[False])[:30]
labels=price1['品牌'][:10]
df1 = df1.drop(df1[[xx not in list(labels) for xx in df1['品牌']]].index)
dfs = ['' for i in range(6)]
dfs[0]=df1[df['价格等级']=='0~999']
dfs[1]=df1[df['价格等级']=='1000~1999']
dfs[2]=df1[df['价格等级']=='1999~2999']
dfs[3]=df1[df['价格等级']=='2999~3999']
dfs[4]=df1[df['价格等级']=='3999~4999']
dfs[5]=df1[df['价格等级']=='5000+']

bottoms = [[] for xx in range(6)]
values = ['' for xx in range(6)]
for ii in range(6):
    tmp = dfs[ii].groupby('品牌')['累计评价数'].sum().reset_index()
    values[ii] = [0 if xx not in list(tmp['品牌']) else tmp[tmp['品牌'] == xx]['累计评价数'].sum() for xx in labels]
    # print(values[ii])
    if ii == 0:
        bottoms[ii] = [0 for xx in range(10)]
    else:
        bottoms[ii] = [bottoms[ii-1][xx] + list(values[ii-1])[xx] for xx in range(int(N))]
ind = np.arange(N)  # the x locations for the groups
width = 0.5  # the width of the bars: can also be len(x) sequence

ps = [None for xx in range(6)]
for ii in range(6):
    ps[ii] = plt.bar(ind,values[ii],width,bottoms[ii])

plt.ylabel('销量')
plt.title('总销量Top10手机品牌价格构成')
plt.gcf().subplots_adjust(bottom=0.2)
plt.xticks(ind, labels, fontsize=10,rotation=75)
# plt.yticks(np.arange(0, 81, 20))
plt.legend((ps[0][0], ps[1][0], ps[2][0],ps[3][0],ps[4][0],ps[5][0]),
           ('0~999', '1000~1999','1999~2999', '2999~3999','3999~4999','5000+'))
plt.savefig('总销量Top10手机品牌价格构成')
plt.show()
