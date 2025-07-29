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
X = pd.concat([market_rf, pivot], axis=1).dropna().drop(columns=['Eco_Treasury', 'Market Cap', 'Revenue', 'Community'])
X = sm.add_constant(X)
print("X name:")
print(X.columns.tolist())
print("\nX data ex:")
print(X.head())

# Step 4: y
y = df['ARB'].dropna()
y.index = X.index

# Step 5: Regression
model = sm.OLS(y, X).fit()
print(model.summary())

# -------------------------------------------
# Step 6: VIF
print("\n=== Variance Inflation Factor (VIF) ===")
vif_data = pd.DataFrame()
vif_data['Variable'] = X.columns
vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

# Step 7: Residual analysis
from statsmodels.stats.diagnostic import het_breuschpagan, acorr_breusch_godfrey

# heteroskedasticity
bp_test = het_breuschpagan(model.resid, model.model.exog)
print(f"\nBreusch-Pagan p-value (Heteroskedasticity): {bp_test[1]:.4f}")

# autocorrelation
bg_test = acorr_breusch_godfrey(model, nlags=4)
print(f"\nBreusch-Godfrey p-value (Autocorrelation): {bg_test[3]:.4f}")

# Step 8: visualization
plt.figure(figsize=(10, 4))
sns.histplot(model.resid, bins=20, kde=True)
plt.title("Residual Distribution")
plt.show()

