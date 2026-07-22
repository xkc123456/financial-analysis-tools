# -*- coding: utf-8 -*-
"""
回归分析演示 —— 模拟 Stata 的 reg 命令
主题：数字化转型对审计质量的影响
"""

import numpy as np
import pandas as pd

# ========== 1. 生成模拟数据 ==========
np.random.seed(42)
n = 500

data = pd.DataFrame({
    '公司ID': range(1, n+1),
    '数字化程度': np.random.uniform(0, 100, n),
    '企业规模': np.random.uniform(10, 25, n),
    '资产负债率': np.random.uniform(0.2, 0.8, n),
    '是否四大审计': np.random.choice([0, 1], n, p=[0.7, 0.3]),
})

# 构造 Y = 审计费用
data['审计费用'] = (
    2.0 + 0.03 * data['数字化程度'] + 0.15 * data['企业规模']
    + 0.5 * data['资产负债率'] + 0.8 * data['是否四大审计']
    + np.random.normal(0, 1.5, n)
)

print("=" * 70)
print("回归分析：数字化转型对审计质量的影响")
print("=" * 70)
print(f"样本量: {n}\n")
print(data.head().to_string(index=False))

# ========== 2. 跑回归 ==========
import statsmodels.api as sm

X = data[['数字化程度', '企业规模', '资产负债率', '是否四大审计']]
X = sm.add_constant(X)
y = data['审计费用']
model = sm.OLS(y, X).fit()

# ========== 3. 输出结果表 ==========
print("\n" + "=" * 70)
print("回归结果（Stata 风格）")
print("=" * 70)
print(f"{'变量':<20} {'系数':>10} {'标准误':>10} {'t值':>10} {'p值':>10} {'':>6}")
print("-" * 70)

for var in model.params.index:
    coef = model.params[var]
    se = model.bse[var]
    t = model.tvalues[var]
    p = model.pvalues[var]
    sig = '***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.1 else ''
    print(f"{var:<20} {coef:>10.4f} {se:>10.4f} {t:>10.2f} {p:>10.4f} {sig:>6}")

print("-" * 70)
print(f"{'R²':<20} {model.rsquared:>10.4f}")
print(f"{'调整后R²':<20} {model.rsquared_adj:>10.4f}")
print(f"{'F统计量':<20} {model.fvalue:>10.2f}")
print(f"{'F检验p值':<20} {model.f_pvalue:>10.4f}")

# ========== 4. 解读 ==========
print("\n" + "=" * 70)
print("解读")
print("=" * 70)
for var in model.params.index:
    if var == 'const':
        continue
    coef = model.params[var]
    p = model.pvalues[var]
    if p < 0.05:
        print(f"  ✅ {var} 显著(p={p:.4f}) 系数={coef:.4f}")
    elif p < 0.1:
        print(f"  ⚠️  {var} 边缘显著(p={p:.4f}) 系数={coef:.4f}")
    else:
        print(f"  ❌ {var} 不显著(p={p:.4f}) 系数={coef:.4f}")

print(f"\n结论：数字化程度每提高1，审计费用增加{model.params['数字化程度']:.4f}")
print(f"R²={model.rsquared:.3f}，模型解释力{model.rsquared*100:.1f}%")
