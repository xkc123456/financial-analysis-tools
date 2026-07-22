* ================================================
* 实证分析进阶：导出结果 + 诊断检验
* 方向1：用 esttab 把回归结果导出到 Word
* 方向3：异方差检验 + 多重共线性检验
* ================================================

clear all
set more off

* ========== 先用练习数据跑回归 ==========
import delimited "C:\Users\Xing\Documents\Codex\2026-07-10\nin\outputs\练习数据.csv", clear encoding("utf-8")
encode industry, gen(ind_cat)

* ====== 方向1：esttab 导出到 Word ======

* 第一步：跑回归并起名存储
reg audit_fee size profit debt
estimates store model_basic

* 第二步：再加一个带行业控制的模型
reg audit_fee size profit debt i.ind_cat
estimates store model_full

* 第三步：安装 estout（只需装一次）
* ssc install estout, replace

* 第四步：导出到 Word（RTF格式）
* 这行会生成一个 .rtf 文件，Word 可以直接打开
esttab model_basic model_full ///
    using "审计费用回归结果.rtf", replace ///
    title("表1：审计费用影响因素的回归结果") ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    b(3) se(3) ///
    stats(N r2 F, fmt(0 3 2) ///
        labels("样本量" "R²" "F值")) ///
    mtitles("基础模型" "加入行业控制") ///
    notes("注：括号内为标准误；*** p<0.01, ** p<0.05, * p<0.10")

display "===== 方向1完成：结果已导出到 审计费用回归结果.rtf ====="


* ====== 方向3：诊断检验 ======
display ""
display "======== 方向3：回归诊断检验 ========"

* 先跑一个完整的回归
reg audit_fee size profit debt i.ind_cat

* ---------- 检验1：异方差 ----------
* 异方差 = 误差项的方差不恒定
* 比如大公司的审计费用波动更大，小公司更稳定——这就叫异方差
* 存在异方差时，标准误可能有偏，系数显著性不可靠

display ""
display "------ 检验1：异方差（Breusch-Pagan / Cook-Weisberg）------"
estat hettest
* 原假设 H0：同方差（没有异方差）
* 如果 p < 0.05，拒绝 H0 → 存在异方差

display ""
display "------ 异方差补充检验：White 检验 ------"
* White 检验更全面，能检测非线性形式的异方差
* imtest, white
* （如果装了 imtest 可用，否则用 estat hettest 即可）


* ---------- 检验2：多重共线性 ----------
* 多重共线性 = 自变量之间高度相关
* 比如"企业规模"和"资产负债率"高度相关——你的模型无法区分它俩各自的影响
* VIF（方差膨胀因子）> 10 通常认为存在严重共线性
* VIF > 5 需要关注

display ""
display "------ 检验2：多重共线性（VIF）------"
estat vif
* VIF = 1 / (1 - R²_j)  其中 R²_j 是把这个X对其他所有X回归得到的R²
* VIF > 10 → 严重共线性，需要考虑删变量或用岭回归


* ---------- 检验3：模型设定错误 ----------
display ""
display "------ 检验3：Ramsey RESET 检验 ------"
estat ovtest
* 原假设 H0：模型没有遗漏重要非线性项
* 如果 p < 0.05 → 模型可能设错了（遗漏了平方项或交互项）


* ====== 小结 ======
display ""
display "==================================="
display "实证分析进阶总结"
display "==================================="
display ""
display "1. esttab：把 Stata 回归结果变成论文格式的 Word 表格"
display "   - 可以同时放多个模型对比（基础 vs 加控制变量）"
display "   - 自动加星号、标准误、样本量、R²"
display ""
display "2. 诊断检验三步走："
display "   - estat hettest → 异方差（误差是否稳定）"
display "   - estat vif → 多重共线性（X之间是否太相关）"
display "   - estat ovtest → 模型设定是否正确"
display ""
display "3. 一般论文的实证流程："
display "   描述统计 → 基准回归 → 加入控制变量 → 诊断检验 → 稳健性检验"
