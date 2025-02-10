import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

def analyze_bond_data(csv_file):
    """分析债券数据"""
    # 读取CSV文件
    df = pd.read_csv(csv_file)
    
    # 1. 基本统计信息
    print("\n=== 基本统计信息 ===")
    print(f"总记录数: {len(df)}")
    
    # 2. 按月份统计发行数量
    df['Issue Date'] = pd.to_datetime(df['Issue Date'])
    df['Month'] = df['Issue Date'].dt.strftime('%Y-%m')
    monthly_count = df.groupby('Month').size()
    
    print("\n=== 月度发行统计 ===")
    print(monthly_count)
    
    # 3. 发行机构分析
    issuer_count = df['Issuer'].value_counts()
    print("\n=== 发行机构统计 ===")
    print(issuer_count)
    
    # 4. 可视化
    plt.figure(figsize=(12, 6))
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 月度发行量趋势图
    monthly_count.plot(kind='bar', color='skyblue')
    plt.title('2023年国债月度发行量趋势', fontsize=12, pad=15)
    plt.xlabel('发行月份')
    plt.ylabel('发行数量(只)')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 添加数值标签
    for i, v in enumerate(monthly_count):
        plt.text(i, v, str(v), ha='center', va='bottom')
    
    # 添加图表说明
    plt.figtext(0.02, 0.02, 
                '数据来源: 中国货币网\n' + 
                f'统计时间: {datetime.now().strftime("%Y-%m-%d")}\n' +
                '说明: 统计2023年发行的国债(Treasury Bond)数据',
                fontsize=8)
    
    # 保存图表
    plt.tight_layout()
    plt.savefig('bond_analysis.png', dpi=300, bbox_inches='tight')
    
    # 5. 导出分析结果
    analysis_results = {
        '月度统计': monthly_count.to_dict(),
        '发行机构统计': issuer_count.to_dict()
    }
    
    # 导出为Excel，包含多个sheet
    with pd.ExcelWriter('bond_analysis.xlsx') as writer:
        df.to_excel(writer, sheet_name='原始数据', index=False)
        monthly_count.to_frame('发行数量').to_excel(writer, sheet_name='月度统计')
        issuer_count.to_frame('发行数量').to_excel(writer, sheet_name='发行机构统计')
    
    return analysis_results

if __name__ == "__main__":
    # 使用最新生成的CSV文件
    csv_file = 'test/treasury_bonds_20250210_101140.csv'  # 替换为您的文件名
    
    print("开始分析债券数据...")
    results = analyze_bond_data(csv_file)
    
    print("\n分析完成！生成了以下文件：")
    print("1. bond_analysis.xlsx - 详细分析结果")
    print("2. bond_analysis.png - 数据可视化图表")