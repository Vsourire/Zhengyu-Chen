import pandas as pd

# === Load Excel  ===
file_path = "C:\\Users\\13013\\Desktop\\Dissertation\\Zhengyu-Chen\\datasheet.v3.xlsx"  
xls = pd.ExcelFile(file_path)

# sheet names
factor_sheets = [
    "Gov", "Users", "Community", "Revenue", 
    "Treasury_MarketCap", "Develop", "DEFX market"
]

# load factor data
factor_data = {sheet: xls.parse(sheet) for sheet in factor_sheets}
returns_daily = xls.parse("ReturnDaily")

# === clean data ===
factor_long = []
for name, df in factor_data.items():
    df_long = df.melt(id_vars='Date', var_name='DAO', value_name='Score')
    df_long['Factor'] = name
    factor_long.append(df_long)
factor_all = pd.concat(factor_long, ignore_index=True)

returns = returns_daily.rename(columns={"DAO": "Date"}, inplace=True) 
returns_long = returns_daily.melt(id_vars='Date', var_name='DAO', value_name='Return')

factor_all['Date'] = pd.to_datetime(factor_all['Date'])
returns_long['Date'] = pd.to_datetime(returns_long['Date'])

# === HML return ===
all_results = []

for factor_name, factor_df in factor_all.groupby('Factor'):
  
    for week_date, week_group in factor_df.groupby('Date'):
     
        week_group = week_group.dropna(subset=['Score'])
        if len(week_group) < 10:
            continue

        # Score Rank
        sorted_group = week_group.sort_values('Score', ascending=False)
        n = len(sorted_group)
        top_n = int(n * 0.3)
        bottom_n = int(n * 0.3)
        top30_daos = sorted_group.head(top_n)['DAO'].tolist()
        bottom30_daos = sorted_group.tail(bottom_n)['DAO'].tolist()

        next_week_date = factor_df[factor_df['Date'] > week_date]['Date'].min()
        if pd.isna(next_week_date):
            
            end_date = returns_long['Date'].max()
        else:
            end_date = next_week_date - pd.Timedelta(days=1)

        
        mask = (returns_long['Date'] >= week_date) & (returns_long['Date'] <= end_date)

        daily_top = returns_long[mask & returns_long['DAO'].isin(top30_daos)]
        daily_bottom = returns_long[mask & returns_long['DAO'].isin(bottom30_daos)]

        
        top_daily_mean = daily_top.groupby('Date')['Return'].mean()
        bottom_daily_mean = daily_bottom.groupby('Date')['Return'].mean()

        
        factor_daily_return = top_daily_mean - bottom_daily_mean

        
        temp_df = pd.DataFrame({
            'Date': factor_daily_return.index,
            'Factor': factor_name,
            'Top30_MeanReturn': top_daily_mean.values,
            'Bottom30_MeanReturn': bottom_daily_mean.values,
            'FactorReturn': factor_daily_return.values
        })
        all_results.append(temp_df)


factor_returns_daily_df = pd.concat(all_results, ignore_index=True)
factor_returns_daily_df.sort_values(['Date', 'Factor'], inplace=True)
factor_returns_daily_df.to_excel("factor_returns_daily_v1.xlsx", index=False)