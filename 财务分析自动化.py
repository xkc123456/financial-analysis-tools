# -*- coding: utf-8 -*-
"""
财务分析自动化脚本 v2.0 - 自动生成可视化HTML报告
会计学学生 · 第一份作品 · 一键生成 · 无需手动操作
"""

import json
import os
import webbrowser
from datetime import datetime

# ========== 1. 内置三家公司财务数据 ==========
data = {
    "格力电器(制造)": {
        "revenue": 2036, "cogs": 1470, "sellExp": 125, "adminExp": 56,
        "finExp": -28, "tax": 32, "assets": 3682, "liab": 2090, "equity": 1592,
        "desc": "高利润率+较低杠杆，典型的制造型企业盈利能力驱动ROE",
        "type": "green"
    },
    "永辉超市(零售)": {
        "revenue": 910, "cogs": 730, "sellExp": 140, "adminExp": 22,
        "finExp": 12, "tax": 1.5, "assets": 520, "liab": 388, "equity": 132,
        "desc": "低利润率+高周转+高杠杆，零售业靠规模和周转吃饭",
        "type": "red"
    },
    "恒瑞医药(科技)": {
        "revenue": 232, "cogs": 30, "sellExp": 70, "adminExp": 22,
        "finExp": -3, "tax": 10, "assets": 400, "liab": 48, "equity": 352,
        "desc": "极高利润率+极低杠杆，轻资产高科技企业特征",
        "type": "green"
    }
}

# ========== 2. 计算指标 ==========
def calc(d):
    gp = d["revenue"] - d["cogs"]
    op = gp - d["sellExp"] - d["adminExp"]
    np_val = op - d["finExp"] - d["tax"]
    return {
        "roe": round(np_val / d["equity"] * 100, 2),
        "npm": round(np_val / d["revenue"] * 100, 2),
        "at": round(d["revenue"] / d["assets"], 3),
        "em": round(d["assets"] / d["equity"], 2),
        "gm": round(gp / d["revenue"] * 100, 2),
        "opm": round(op / d["revenue"] * 100, 2),
        "debt": round(d["liab"] / d["assets"] * 100, 2),
        "np": round(np_val, 1),
        "op": round(op, 1)
    }

results = {name: calc(d) for name, d in data.items()}

# ========== 3. 生成 HTML 报告 ==========
report = []
report.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>自动化财务分析报告</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',-apple-system,Roboto,sans-serif;background:#f1f5f9;color:#1e293b;padding:20px;}
.container{max-width:1200px;margin:0 auto;}
.header{background:linear-gradient(135deg,#1e3a5f,#2563eb);color:#fff;border-radius:16px;padding:28px 32px;margin-bottom:20px;}
.header h1{font-size:26px;font-weight:700;margin-bottom:6px;}
.header p{font-size:14px;opacity:0.8;}
.header .meta{display:flex;gap:20px;margin-top:12px;font-size:12px;opacity:0.7;}
h2{font-size:16px;font-weight:600;margin-bottom:12px;display:flex;align-items:center;gap:8px;margin-top:20px;}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:16px;margin-bottom:20px;}
.card{background:#fff;border-radius:12px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.08);}
.card h3{font-size:15px;font-weight:700;margin-bottom:12px;display:flex;justify-content:space-between;}
.roe{display:inline-flex;align-items:center;gap:4px;font-size:20px;font-weight:800;}
.roe.green{color:#10b981;}
.roe.yellow{color:#f59e0b;}
.roe.red{color:#ef4444;}
.metrics{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.metric{background:#f8fafc;border-radius:8px;padding:10px;}
.metric .lbl{font-size:11px;color:#64748b;}
.metric .val{font-size:18px;font-weight:700;}
.metric .pct{font-size:13px;color:#64748b;font-weight:400;}
.desc{font-size:12px;color:#64748b;margin-top:10px;padding:8px 10px;border-radius:6px;border-left:3px solid #10b981;background:#f0fdf4;}
.desc.warn{background:#fffbeb;border-color:#f59e0b;}

table{width:100%;border-collapse:collapse;font-size:13px;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:20px;}
th{background:#f8fafc;text-align:left;padding:10px 12px;font-weight:600;color:#475569;border-bottom:2px solid #e2e8f0;}
td{padding:10px 12px;border-bottom:1px solid #f1f5f9;}
tr:last-child td{border-bottom:none;}

.dupont{background:#fff;border-radius:12px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:20px;}
.dup-row{display:flex;align-items:center;gap:8px;margin-bottom:6px;padding:6px 8px;background:#f8fafc;border-radius:6px;font-size:13px;}
.dup-row .op{color:#94a3b8;}
.dup-row .nv{font-weight:700;min-width:60px;text-align:right;}
.fml{background:#f1f5f9;border-radius:8px;padding:12px;font-size:12px;color:#475569;line-height:1.6;margin-top:8px;}
.footer{text-align:center;font-size:12px;color:#94a3b8;margin:20px 0;}
.tag{display:inline-block;font-size:11px;padding:2px 8px;border-radius:4px;margin-left:6px;}
.tag.green{background:#d1fae5;color:#065f46;}
.tag.yellow{background:#fef3c7;color:#92400e;}
.tag.red{background:#fee2e2;color:#991b1b;}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>📊 自动化财务分析报告</h1>
<p>基于杜邦分析框架 · 三家公司横向对比 · 一键生成</p>
<div class="meta">
<span>📅 """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """</span>
<span>📁 分析工具：Python 财务分析脚本 v2.0</span>
</div>
</div>
""")

# Cards
report.append('<h2>🏢 公司财务全景</h2><div class="grid">')
for name, d in data.items():
    r = results[name]
    roe_cls = "green" if r["roe"] >= 15 else ("yellow" if r["roe"] >= 5 else "red")
    desc_cls = "warn" if d["type"] == "red" else ""
    report.append(f'''
<div class="card">
<h3><span>{name}</span><span class="roe {roe_cls}">{r["roe"]:.1f}%</span></h3>
<div class="metrics">
  <div class="metric"><div class="lbl">销售净利率</div><div class="val">{r["npm"]:.1f}<span class="pct">%</span></div></div>
  <div class="metric"><div class="lbl">资产周转率</div><div class="val">{r["at"]:.2f}<span class="pct"> 次</span></div></div>
  <div class="metric"><div class="lbl">权益乘数</div><div class="val">{r["em"]:.2f}<span class="pct"> ×</span></div></div>
  <div class="metric"><div class="lbl">资产负债率</div><div class="val">{r["debt"]:.1f}<span class="pct">%</span></div></div>
  <div class="metric"><div class="lbl">毛利率</div><div class="val">{r["gm"]:.1f}<span class="pct">%</span></div></div>
  <div class="metric"><div class="lbl">净利润(万元)</div><div class="val">{r["np"]:.0f}</div></div>
</div>
<div class="desc {desc_cls}">{d["desc"]}</div>
</div>
''')
report.append('</div>')

# Compare table
report.append('<h2>📋 核心指标对比</h2>')
report.append('<table><thead><tr><th>指标</th>')
for name in data:
    report.append(f'<th>{name}</th>')
report.append('</tr></thead><tbody>')

fields = [("roe","ROE(%)"),("npm","净利率(%)"),("gm","毛利率(%)"),("opm","营业利润率(%)"),
          ("at","资产周转率"),("em","权益乘数"),("debt","资产负债率(%)")]
for key, label in fields:
    report.append(f'<tr><td style="font-weight:600;">{label}</td>')
    for name in data:
        v = results[name][key]
        display = f"{v:.2f}" if key in ("at","em") else f"{v:.1f}"
        report.append(f'<td>{display}</td>')
    report.append('</tr>')
report.append('</tbody></table>')

# DuPont
report.append('<h2>🔍 杜邦公式展开</h2><div class="dupont">')
for name in data:
    r = results[name]
    check = abs(r["roe"] - (r["npm"]/100 * r["at"] * r["em"] * 100)) < 0.05
    report.append(f'''
<h3 style="margin:12px 0 6px;">{name}</h3>
<div class="dup-row"><span>ROE</span><span class="op">=</span><span class="nv" style="color:{'#10b981' if r['roe']>=15 else '#f59e0b'};">{r["roe"]:.1f}%</span></div>
<div class="dup-row" style="padding-left:24px;">
  <span>{r["npm"]:.1f}%</span><span class="op">×</span>
  <span>{r["at"]:.3f}</span><span class="op">×</span>
  <span>{r["em"]:.2f}</span>
</div>
<div class="fml">验算：{r["npm"]:.1f}% × {r["at"]:.3f} × {r["em"]:.2f} = {(r["npm"]/100 * r["at"] * r["em"] * 100):.1f}%
  → {"✅ 一致" if check else "❌ 偏差"}
</div>
''')
report.append('</div>')

# Insights
report.append('<h2>📝 自动化解读</h2>')
report.append('<table><thead><tr><th>公司</th><th>驱动类型</th><th>特征</th><th>风险提示</th></tr></thead><tbody>')
for name in data:
    r = results[name]
    if r["npm"] > 15:
        driver = "<span class='tag green'>高利润率驱动</span>"
    elif r["at"] > 1 and r["npm"] < 5:
        driver = "<span class='tag yellow'>高周转驱动</span>"
    elif r["em"] > 3:
        driver = "<span class='tag yellow'>高杠杆驱动</span>"
    else:
        driver = "<span class='tag green'>均衡驱动</span>"

    if r["debt"] > 70:
        risk = "<span class='tag red'>负债率偏高</span>"
    elif r["debt"] > 50:
        risk = "<span class='tag yellow'>杠杆适中</span>"
    else:
        risk = "<span class='tag green'>财务保守</span>"

    report.append(f'<tr><td style="font-weight:600;">{name}</td><td>{driver}</td><td style="font-size:12px;">{data[name]["desc"]}</td><td>{risk}</td></tr>')
report.append('</tbody></table>')

report.append('<div class="footer">自动化财务分析报告 · 基于 Python 自动生成</div>')
report.append('</div></body></html>')

# ========== 4. 保存并打开 ==========
html_content = "\n".join(report)
out_path = os.path.join(os.path.dirname(__file__) or ".", "财务分析报告_自动生成.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("")
print("=" * 50)
print("📊 自动化财务分析报告 ｜ 完整版")
print("=" * 50)
print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"输出文件：{out_path}")
print("")
print("📋 核心指标一览")
print("-" * 50)
print(f"{'公司':<16}{'ROE%':<10}{'净利率%':<10}{'周转率':<10}{'杠杆':<10}{'负债率%':<10}")
print("-" * 50)
for name in data:
    r = results[name]
    mark = "✅" if r["roe"] >= 15 else ("⚠️" if r["roe"] >= 5 else "❌")
    print(f"{name:<14}  {mark} {r['roe']:<6.1f}  {r['npm']:<8.1f}  {r['at']:<8.3f}  {r['em']:<8.2f}  {r['debt']:<8.1f}")
print("-" * 50)
print("")
print(f"✅ 可视化报告已自动生成：{out_path}")
print("💡 双击该HTML文件即可在浏览器中查看完整报告")
