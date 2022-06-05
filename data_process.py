import pandas as pd
import numpy as np

phone = pd.read_csv('data/cellphone.csv')
add_comments = pd.read_csv('data/count_add_comments.csv')

assert (phone is not None)
assert (add_comments is not None)

# 删除空白列
phone = phone.drop(columns=['Unnamed: 19'])

# 先获取列名，在此基础上进行更改
print(phone.columns)
phone.columns = ['爬取时间', '爬取链接', '商品ID', '商品名称',
                 '商品描述', '商品参数', '商品现价',
                 '商品原价', '月销量', '库存',
                 '发货地址', '商品发布时间',
                 '店铺ID', '店铺名称', '商品链接URL', '评分',
                 '收藏数', '累计评价数', '商品评价印象标签']
print(phone.columns)
# 商品描述、月销量、库存、评分、累计评价数存在缺失

# 查看月销量为0的商品信息
print(phone[phone['月销量'].isnull()].info())
# 对销量为零的数据进行 0 填充
phone['月销量'] = phone['月销量'].fillna(0)

# 处理库存（0 填充）、评分（删除空白数据）、累计评价数（0填充）
phone['库存'] = phone['库存'].fillna(0)
phone['累计评价数'] = phone['累计评价数'].fillna(0)
phone = phone.dropna(subset=['评分'])

# 重新梳理 index
phone.index = np.arange(len(phone))

# add_comments和 phone 进行数据合并
df = pd.merge(phone, add_comments, left_on='商品ID', right_on='ID(id)')

df.columns = ['爬取时间', '爬取链接', '商品ID', '商品名称',
              '商品描述', '商品参数', '商品现价',
              '商品原价', '月销量', '库存',
              '发货地址', '商品发布时间',
              '店铺ID', '店铺名称', '商品链接URL', '评分',
              '收藏数', '累计评价数', '商品评价印象标签', '图片', '追评', 'ID(id)', 'Unnamed: 3']
df = df.drop(columns=['Unnamed: 3'])
df = df.drop(columns=['ID(id)'])

# -------------修改时间格式--------------
import time

df['商品发布时间'] = df['商品发布时间'].apply(lambda op: time.strftime('%Y-%m-%d', time.localtime(op)))


# ----------------清洗价格--------------
def get_price(s):
    price = s.split('-')
    l = [float(i) for i in price]
    return np.mean(l)


df['商品现价'] = df['商品现价'].apply(get_price)
df['商品原价'] = df['商品原价'].apply(get_price)


# -----------------清洗发货城市--------------------
# 获得中国全部的省级单位名称，找到全部的省级单位
# 将每一个地址的省份提取出来，剩下的就是城市
pro_list = ['北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北',
            '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '内蒙古', '广西', '西藏', '宁夏', '新疆', '香港', '澳门']


def get_city(address):
    for i in pro_list:
        if i in address:
            city = address.replace(i, '')
            if len(city) == 0:
                city = i
            return city


def get_province(address):
    for i in pro_list:
        if i in address:
            province = i
            return province


df['发货城市'] = df['发货地址'].apply(get_city)
df['发货省份'] = df['发货地址'].apply(get_province)

# ---------------价格分箱------------------
import matplotlib.pyplot as plt
price_=df['商品现价'].value_counts().sort_index()
plt.plot(price_.index,price_)
plt.show()

# 创建价格区间
def get_price_level(p):
    level=p//1000
    if level==0:
        return '0~999'
    if level==1:
        return '1000~1999'
    if level==2:
        return '1999~2999'
    if level==3:
        return '2999~3999'
    if level==4:
        return '3999~4999'
    if level>=5:
        return '5000+'
    else:
        return '计算出错'
df['价格等级']=df['商品现价'].apply(get_price_level)

# ---------------手机参数信息提取------------
target=['后置摄像头', '摄像头类型', '视频显示格式', '分辨率', '触摸屏类型', '屏幕尺寸', '网络类型',
 '网络模式', '键盘类型', '款式', '运行内存RAM', '存储容量', '品牌', '华为型号', '电池类型',
 '核心数', '机身颜色', '手机类型', '操作系统', 'CPU品牌', '产品名称']
for t in target:
    def get_pram(p):
        for i in eval(p):
            if i['label']==t:
                return i['value']
    df[t]=df['商品参数'].apply(get_pram)

