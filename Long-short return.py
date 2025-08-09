import pandas as pd

# === 1. Load Excel  ===
file_path = "C:\\Users\\13013\\Desktop\\Dissertation\\Zhengyu-Chen\\datasheet.v3.xlsx"  # 改成你本地文件路径
xls = pd.ExcelFile(file_path)

# sheet names
factor_sheets = [
    "Gov", "Users", "Community", "Revenue", 
    "Treasury_MarketCap", "Develop", "DEFX market"
]

# load factor data
factor_data = {sheet: xls.parse(sheet) for sheet in factor_sheets}
returns = xls.parse("Return")

# === 2. clean data ===
factor_long = []
for name, df in factor_data.items():
    df_long = df.melt(id_vars='Date', var_name='DAO', value_name='Score')
    df_long['Factor'] = name
    factor_long.append(df_long)
factor_all = pd.concat(factor_long, ignore_index=True)

returns = returns.rename(columns={"DAO": "Date"})  
returns_long = returns.melt(id_vars='Date', var_name='DAO', value_name='Return')

# === 3. Merge and Score ===
merged = pd.merge(factor_all, returns_long, on=['Date', 'DAO'], how='inner')

# === 4. HML return ===
def calculate_factor_return(df):
    results = []

    for (date, factor), group in df.groupby(['Date', 'Factor']):
        group = group.dropna(subset=['Score', 'Return'])
        if len(group) < 10:
            continue  

        # Score Rank
        group_sorted = group.sort_values('Score', ascending=False)
        n = len(group_sorted)
        top_n = int(n * 0.3)
        bottom_n = int(n * 0.3)

        top30 = group_sorted.head(top_n)
        bottom30 = group_sorted.tail(bottom_n)

        top_return = top30['Return'].mean()
        bottom_return = bottom30['Return'].mean()
        hml = top_return - bottom_return

        results.append({
            'Date': date,
            'Factor': factor,
            'Top30_MeanReturn': top_return,
            'Bottom30_MeanReturn': bottom_return,
            'FactorReturn': hml
        })

    return pd.DataFrame(results)

factor_returns_df = calculate_factor_return(merged)

# === 5. Result ===
factor_returns_df.sort_values(['Date', 'Factor']).to_excel("factor_returns_output_v1.xlsx", index=False)

