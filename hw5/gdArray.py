import gd as gd  # 將梯度下降模組 gd 導入程式
from micrograd.engine import Value  # 從 micrograd.engine 模組導入 Value 類

# 定義目標函數 f，輸入為參數向量 p
def f(p):
    [x, y, z] = p  # 將向量 p 解包成 x, y, z
    
    return (x-2)**2 + 3*(y-0.5)**2 + (z-3)**2  # 返回新的目標函數值

# 初始化參數向量 p，使用 micrograd 的 Value 類包裝初始值
p = [Value(2.0), Value(1.0), Value(3.0)]

# 呼叫梯度下降方法來尋找目標函數的最小值，並打印結果
print(gd.gradientDescendent(f, p))