import numpy as np  
import matplotlib.pyplot as plt  

# 设置字体大小  
font_size = 12  

# 加载数据  
ther1_kappa = np.loadtxt('1_kappa.out')  
ther2_kappa = np.loadtxt('2_kappa.out')  
#ther3_kappa = np.loadtxt('3_kappa.out')  

# 获取数据的行数  
M1 = ther1_kappa.shape[0]  
M2 = ther2_kappa.shape[0]  
#M3 = ther3_kappa.shape[0]  

# 确保所有文件的行数相同以便后续计算  
if not (M1 == M2):  
    raise ValueError("文件行数不一致，请检查输入数据。")  

# 计算热导率（x方向）  
kappa_x_1 = ther1_kappa[:, 2] + ther1_kappa[:, 3]  
kappa_x_2 = ther2_kappa[:, 2] + ther2_kappa[:, 3]  
#kappa_x_3 = ther3_kappa[:, 0] + ther3_kappa[:, 1]  

# 计算累积平均值  
kxi_ave_1 = np.cumsum(kappa_x_1) / np.arange(1, M1 + 1)  
kxi_ave_2 = np.cumsum(kappa_x_2) / np.arange(1, M2 + 1)  
#kxi_ave_3 = np.cumsum(kappa_x_3) / np.arange(1, M3 + 1)  

# 计算总的平均线  
avg_kappa_total = np.mean([kxi_ave_1, kxi_ave_2], axis=0)  

# 计算标准误  
rtc_x = np.array([kxi_ave_1, kxi_ave_2])  
rtc_x_ave = np.mean(rtc_x, axis=0)  
rtc_x_err = np.std(rtc_x, axis=0, ddof=1) / np.sqrt(len(rtc_x))  # M = len(rtc_x)  

# 计算 kappa 值及其误差  
N = len(rtc_x_ave)  
kappa_x = np.mean(rtc_x_ave[4*N//5:5*N//5])  # 对应MATLAB的: 1*end/5:2*end/5  
kappa_err_x = np.mean(rtc_x_err[4*N//5:5*N//5])  
#kappa_y = np.mean(rtc_y_ave[2*N//3:3*N//4])  # 对应MATLAB的: 2*end/3:3*end/4  
#kappa_err_y = np.mean(rtc_y_err[2*N//3:3*N//4])  
#kappa_tot = (kappa_x + kappa_y) / 2  
#kappa_err_tot = (kappa_err_y + kappa_err_x) / 2  

# 时间轴  
t = np.arange(1, M1 + 1) * 0.001  # 假设每步时间为0.001ns  

# 绘图  
plt.figure(figsize=(8, 4))  # 根据需要设置图形大小  

# 绘制 y 方向的热导率  
plt.plot(t, kxi_ave_1, 'gray', linewidth=2, alpha=0.5)  
plt.plot(t, kxi_ave_2, 'gray', linewidth=2, alpha=0.5, label='Cycles')  
#plt.plot(t, kxi_ave_3, 'gray', linewidth=2, alpha=0.5, label='Cycles')  

# 绘制总的平均线  
plt.plot(t, avg_kappa_total, color='red', linewidth=2.5, label='Average')  

# 绘制误差范围  
plt.fill_between(t, avg_kappa_total - rtc_x_err, avg_kappa_total + rtc_x_err,  
                 color='blue', alpha=0.2, label='Standard Error')  

# 设置标签和标题  
plt.xlabel('Time (ns)', fontsize=font_size)  
plt.ylabel(r'$\kappa(\mathrm{W}\,\mathrm{m}^{-1}\,\mathrm{K}^{-1})$', fontsize=font_size)

# 设置坐标轴的范围  
plt.ylim(0, 2000)  # 根据实际情况调整  
plt.xlim(0, 10)  

# 修改刻度方向  
plt.xticks(np.arange(0, 12, 2), fontsize=16)  
plt.yticks(np.arange(0, 2000, 200), fontsize=16)  
plt.tick_params(axis='x', direction='in', length=6, width=1.5)  # X轴刻度向上  
plt.tick_params(axis='y', direction='in', length=6, width=1.5)  # Y轴刻度向右  

plt.box(True)  # 显示网格  
plt.legend()  # 显示图例  
plt.tight_layout()  # 自适应布局  

# 设置图形边框线宽度为 1.5  
for spine in plt.gca().spines.values():  
    spine.set_linewidth(1.5)  

# 保存图形  
plt.savefig('hnemd1.pdf')  # 保存图形  

# 输出kappa和kappa的误差  
print(f"Kappa_x: {kappa_x:.4f} ± {kappa_err_x:.4f}")  
#print(f"Kappa_y: {kappa_y:.4f} ± {kappa_err_y:.4f}")  
#print(f"Kappa_total: {kappa_tot:.4f} ± {kappa_err_tot:.4f}")