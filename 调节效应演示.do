* 调节效应演示 + Johnson-Neyman 图
* ================================

clear all
set seed 20260722
set obs 500

* 生成自变量 X：风险感知（1-7 量表）
gen risk_perception = runiform(1, 7)

* 生成调节变量 M：AI使用频率（1-7 量表）
gen ai_use = runiform(1, 7)

* 标准化两个变量，生成交互项（中心化处理，避免多重共线性）
egen risk_c = std(risk_perception)
egen ai_use_c = std(ai_use)
gen interaction = risk_c * ai_use_c

* 生成因变量 Y：监管意愿
* Y = 3 + 0.5*X + 0.3*M + 0.8*X*M + 随机误差
gen urge_to_regulate = 3 + 0.5*risk_c + 0.3*ai_use_c + 0.8*interaction + rnormal(0, 1)

* ======== 第一步：描述性统计 ========
summarize risk_perception ai_use urge_to_regulate

* ======== 第二步：跑回归（含交互项） ========
reg urge_to_regulate risk_c ai_use_c interaction

* ======== 第三步：看懂结果 ========
* interaction 的系数显著为正，说明调节效应存在
* AI使用越多，风险感知对监管意愿的影响越强

* ======== 第四步：Johnson-Neyman 图 ========
* 先安装 interflex（只需装一次，装过可以跳过）
* ssc install interflex, replace

* 用 marginsplot 画交互效应图（Stata内置，不需要额外安装）
margins, at(ai_use_c = (-2(0.5)2)) dydx(risk_c)
marginsplot, xdimension(ai_use_c) yline(0) title("调节效应：AI使用程度对风险感知效果的影响") ///
    ytitle("风险感知对监管意愿的边际效应") xtitle("AI使用程度（标准化）") ///
    scheme(s2color)

* ======== 第五步：Johnson-Neyman 正式方法 ========
* 如果装了 interflex，可以用这行出 J-N 图
* interflex risk_c ai_use_c urge_to_regulate, treat(risk_c) moder(ai_use_c)

display "===== 完成 ====="
