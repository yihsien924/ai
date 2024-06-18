import math
import numpy as np
from numpy.linalg import norm

# 使用有限差分法計算函數 f 在點 p 處第 k 個坐標的偏微分
def df(f, p, k, h=0.01):
    p1 = p.copy()         # 複製點 p
    p1[k] = p[k] + h      # 將第 k 個坐標增加一個小量 h
    return (f(p1) - f(p)) / h  # 計算有限差分來近似偏微分

# 計算函數 f 在點 p 處的梯度
def grad(f, p, h=0.01):
    gp = p.copy()         # 複製點 p
    for k in range(len(p)):
        gp[k] = df(f, p, k, h)  # 計算每個坐標的偏微分
    return gp

# 使用梯度下降法尋找函數 f 的最低點
def gradientDescendent(f, p0, h=0.01, max_loops=100000, dump_period=1000):
    p = p0.copy()          # 複製初始點 p0
    print(p)               # 輸出初始點
    for i in range(max_loops):
        fp = f(p)
        fp.backward()      # 計算函數 f 在點 p 處的反向傳播
        gp = []            # 初始化梯度列表
        for value in p:
            gp.append(value.grad)  # 將每個坐標的梯度加入列表
        glen = norm(gp)     # norm = 梯度的長度 (步伐大小)
        if i % dump_period == 0:
            print("gp=", gp)  # 週期性輸出梯度
        if glen < 0.00001:  # 如果步伐已經很小了，就停止
            break
        gh = np.multiply(gp, -1 * h)  # gh = 逆梯度方向的一小步
        p += gh  # 向 gh 方向走一小步
    answer = []
    for k in p:
        answer.append(k.data)  # 將每個坐標的數據加入答案列表
    print(answer)              # 輸出答案
    return p  # 傳回最低點