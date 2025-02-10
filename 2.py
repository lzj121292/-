import re
from datetime import datetime
import pandas as pd

def reg_search(text, regex_list):
    """
    自定义正则匹配函数
    
    Args:
        text: 需要匹配的文本内容
        regex_list: 正则表达式列表
    
    Returns:
        匹配到的结果列表
    """
    results = []
    
    for regex_dict in regex_list:
        result = {}
        
        for key in regex_dict:
            # 根据不同的key使用不同的正则模式
            if key == '标的证券':
                # 匹配股票代码
                pattern = r'股票代码：([0-9]{6}\.(?:SH|SZ|BJ))'
                match = re.search(pattern, text)
                if match:
                    result[key] = match.group(1)
                    
            elif key == '换股期限':
                # 匹配日期范围
                pattern = r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日.*?(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日'
                match = re.search(pattern, text)
                if match:
                    # 提取并格式化日期
                    start_date = f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"
                    end_date = f"{match.group(4)}-{int(match.group(5)):02d}-{int(match.group(6)):02d}"
                    result[key] = [start_date, end_date]
            
            # 可以根据需要添加其他匹配模式
            
        if result:
            results.append(result)
    
    return results

# 测试代码
if __name__ == "__main__":
    # 测试文本
    text = '''
    标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
    有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。
    换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
    之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
    日至 2027 年 6 月 1 日止。
    '''
    
    # 测试正则列表
    regex_list = [{
        '标的证券': '*自定义*',
        '换股期限': '*自定义*'
    }]
    
    # 执行匹配
    results = reg_search(text, regex_list)
    print("匹配结果:", results)