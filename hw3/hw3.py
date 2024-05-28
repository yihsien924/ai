import pulp
import pandas

myprolp = pulp.LpProblem('ans', sense=pulp.LpMaximize)# 創建一個名為 'ans' 的最大化線性規劃問題
# 定義變數 x, y, z，它們都是 PuLP 的變數類型
x =pulp.LpVariable('x')
y =pulp.LpVariable('y')
z =pulp.LpVariable('z')
myprolp += 3*x +2*y + 5*z # 添加目標函數 3*x + 2*y + 5*z 到問題中（最大化）

# 添加條件到問題中
myprolp += (x+y <=10)
myprolp += (2*x+z <=9)
myprolp += (y+2*z<=11)
myprolp += (x>=0)
myprolp += (y>=0)
myprolp += (z>=0)
#解決線性規劃問題
myprolp.solve()

# 打印每個變數的名稱和其解決後的值
for i in myprolp.variables():
    print(i.name, "=", i.varValue)