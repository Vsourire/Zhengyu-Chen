import pandas as pd
import statsmodels.api as sm
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load Excel factor returns data
df = pd.read_excel("C:\\Users\\13013\\Desktop\\Dissertation\\Zhengyu-Chen\\factor_returns_output.xlsx")

# Step 2: construct x: factor columns
df['DEFX-MKT_RF'] = df['DEFXReturn'] - df['Rf Return']
factor_data = df[['Date', 'Factor', 'FactorReturn', 'DEFX-MKT_RF']].dropna(subset=['Factor'])
pivot = factor_data.pivot_table(index='Date', columns='Factor', values='FactorReturn')

# Market return drop duplicates
market_rf = factor_data[['Date', 'DEFX-MKT_RF']].drop_duplicates(subset='Date').set_index('Date')
X = pd.concat([market_rf, pivot], axis=1).dropna()
X = sm.add_constant(X)
print("X name:")
print(X.columns.tolist())
print("\nX data ex:")
print(X.head())

# Step 3: Find all DAO names (those columns not used in factor construction)
y_cols = ['ARB', 'MNT',	'ENS', 'OP', 'COW', 'BAL', 'OGN', '1INCH', 'AAVE', 'LDO', 'GMX', 'SNX', 'DYDX', 'RDNT']

# Step 4: Regression loop
results = []

for dao in y_cols:
    y = df[['Datey', dao]].dropna().set_index('Datey')
    
    # Align y with X by index
    y = y.loc[y.index.intersection(X.index)]
    X_aligned = X.loc[X.index.intersection(y.index)]

    # Ensure same shape
    if len(y) == 0 or len(X_aligned) == 0:
        continue
    
    try:
        model = sm.OLS(y[dao], X_aligned).fit()

        for param in model.params.index:
            results.append({
                'DAO': dao,
                'Para': param,
                'Beta': model.params[param],
                'p': model.pvalues[param],
                'R²': model.rsquared
            })
    except Exception as e:
        print(f"{dao} Failed: {e}")
        continue

# Step 5: Save to Excel
results_df = pd.DataFrame(results)
output_path = "C:\\Users\\13013\\Desktop\\Dissertation\\Zhengyu-Chen\\All DAO result.xlsx"
results_df.to_excel(output_path, index=False)
