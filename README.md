requests>=2.31.0
urllib3>=2.1.0
pandas>=2.1.4
numpy>=1.24.3
pyOpenSSL>=23.2.0
cryptography>=41.0.7
python-dateutil>=2.8.2
pytz>=2023.3 
matplotlib>=3.7.2

 1.test.py 从中国货币网获取债券市场信息
 当用户使用时需修改请求头中的User-Agent
 请求头在开发者工具，网络选项标签，通过所需的信息进行搜素操作后，找到对应的bondmarketlnfolisten请求
 查看 请求头 和请求参数 并对应所写代码进行修改即可
 请求头样式：
 headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'User-Agent': '...',  # 浏览器标识
     'Referer': 'https://iftp.chinamoney.com.cn/english/bdInfo/',
 }
# 请求参数：
 payload = {
     "pageNo": "1",          # 页码
    "pageSize": "15",       # 每页数量
     "bondType": "100001",   # 债券类型（国债）
     "issueYear": "2023",    # 发行年份
   ... 其他请求参数
}

- 数据来源：中国货币网 (https://iftp.chinamoney.com.cn/english/bdInfo/)
- 统计期间：2023年全年
- 数据类型：Treasury Bond (国债)
### 1. 发行规模
- 总发行量：111只国债
- 月均发行量：约9.25只
- 发行节奏：全年保持稳定发行，无明显断档期

### 2. 发行时间分布
- 最早发行日期：2023年1月
- 最近发行日期：2023年12月
- 发行高峰期：12月份（15只）
- 发行低谷期：1月份（6只）
数据解释：isin_code 是债券的唯一标识符，用于识别和跟踪债券的发行和交易。
bond_code 是债券的代码，用于识别和跟踪债券的发行和交易。
issue 是债券的发行机构
bondType 是债券的类型
issue 发行日期
latest_rating 是债券的最新评级
