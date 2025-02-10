import requests
import pandas as pd
from datetime import datetime
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 自定义 SSL 适配器
class CustomHTTPAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.options |= 0x4
        context.check_hostname = False
        kwargs['ssl_context'] = context
        return super(CustomHTTPAdapter, self).init_poolmanager(*args, **kwargs)

def fetch_bond_data():
    url = "https://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN"
    
    # 创建会话并配置
    session = requests.Session()
    adapter = CustomHTTPAdapter()
    session.mount('https://', adapter)
    session.verify = False
    
    # 修改请求头的 Content-Type
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://iftp.chinamoney.com.cn',
        'Referer': 'https://iftp.chinamoney.com.cn/english/bdInfo/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    # 请求参数
    payload = {
        'pageNo': '1',
        'pageSize': '15',
        'isin': '',
        'bondCode': '',
        'issueEnty': '',
        'bondType': '100001',
        'couponType': '',
        'issueYear': '2023',
        'rtngShrt': '',
        'bondSpclPrjctVrty': ''
    }
    
    all_records = []
    
    try:
        print("Sending request with payload:", payload)
        response = session.post(
            url, 
            headers=headers, 
            data=payload,
            verify=False
        )
        response.raise_for_status()
        
        print("\nRequest Headers:", headers)
        print("\nResponse Headers:", dict(response.headers))
        print("\nResponse Status:", response.status_code)
        print("\nResponse Content:", response.text)
        
        data = response.json()
        
        if data['head']['rep_code'] != '200':
            print("获取数据失败:", data['head'].get('rep_message', '未知错误'))
            return None
            
        total_pages = data['data']['pageTotal']
        print(f"总共有 {total_pages} 页数据")
        
        # 处理第一页数据
        all_records.extend(data['data']['resultList'])
        print(f"已获取第 1 页数据")
        
        # 获取剩余页面数据
        for page in range(2, total_pages + 1):
            payload['pageNo'] = page
            response = session.post(
                url, 
                headers=headers, 
                data=payload,
                verify=False
            )
            response.raise_for_status()
            data = response.json()
            
            if data['head']['rep_code'] == '200':
                records = data['data']['resultList']
                all_records.extend(records)
                print(f"已获取第 {page} 页数据")
            else:
                print(f"获取第 {page} 页数据失败")
        
        if not all_records:
            print("未找到符合条件的数据")
            return None
        
        # 创建DataFrame
        df = pd.DataFrame(all_records)
        
        # 选择并重命名列
        columns_needed = {
            'isin': 'ISIN',
            'bondCode': 'Bond Code',
            'entyFullName': 'Issuer',
            'bondType': 'Bond Type',
            'issueStartDate': 'Issue Date',
            'debtRtng': 'Latest Rating'
        }
        
        df = df[columns_needed.keys()].rename(columns=columns_needed)
        
        # 格式化日期
        df['Issue Date'] = pd.to_datetime(df['Issue Date']).dt.strftime('%Y-%m-%d')
        
        # 保存CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'treasury_bonds_{timestamp}.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n数据已保存到 {filename}")
        print(f"总共获取到 {len(df)} 条记录")
        
        return df
        
    except Exception as e:
        print(f"处理数据时出错: {e}")
        print(f"错误类型: {type(e)}")
        import traceback
        print(f"错误详情:\n{traceback.format_exc()}")
        return None

if __name__ == "__main__":
    print("开始获取国债数据...")
    df = fetch_bond_data()
    if df is not None:
        print("\n数据预览:")
        print(df.head())
