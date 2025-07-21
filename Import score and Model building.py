import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load data
df = pd.read_excel("C:\\Users\\13013\\Desktop\\Dissertation\\Zhengyu-Chen\\DAO Score.xlsx")

# Set X and y
X = df[['GovScore', 'CommunityScore', 'CategoryAdjustedScore', 'Revenue']]
y = df['Yield']
X = sm.add_constant(X)

# Data processing（remove NaN & Inf）
df_model = pd.concat([X, y], axis=1)
df_model = df_model.replace([np.inf, -np.inf], np.nan).dropna()

X_clean = df_model.drop(columns=['Yield'])
y_clean = df_model['Yield']

# Model building
model = sm.OLS(y_clean, X_clean).fit()

# Print model summary
print(model.summary())


