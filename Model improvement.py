import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load data
df = pd.read_excel("C:\\Users\\13013\\Desktop\\Dissertation\\Zhengyu-Chen\\DAO Score.xlsx")


# Set X and y
X = df[['GovScore', 'CommunityScore', 
        'EcosystemScore', 'Revenue']]
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

# Ridge Model Improvement
from sklearn.linear_model import RidgeCV

ridge = RidgeCV(alphas=np.logspace(-4, 4, 100), cv=5).fit(X_clean, y_clean)
print("Optimal alpha (λ):", ridge.alpha_)
print("\nRidge coefficients:")
for name, coef in zip(X_clean.columns, ridge.coef_):
    print(f"{name}: {coef:.4f}")
print("\nIntercept:", ridge.intercept_)

# Visualization of residuals
import matplotlib.pyplot as plt

y_pred = model.predict(X_clean)
residuals = y_clean - y_pred

plt.scatter(y_pred, residuals)
plt.axhline(0, linestyle='--', color='red')
plt.xlabel('Predicted')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.show()

from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data["feature"] = X_clean.columns
vif_data["VIF"] = [variance_inflation_factor(X_clean.values, i) for i in range(X_clean.shape[1])]
print(vif_data)
