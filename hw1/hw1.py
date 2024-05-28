import numpy as np    #NumPy函式庫
from random import random, randint, choice

courses = [
{'teacher': '  ', 'name':'　　', 'hours': -1}, # 空堂
{'teacher': '甲', 'name':'機率', 'hours': 2},
{'teacher': '甲', 'name':'線代', 'hours': 3},
{'teacher': '甲', 'name':'離散', 'hours': 3},
{'teacher': '乙', 'name':'視窗', 'hours': 3},
{'teacher': '乙', 'name':'科學', 'hours': 3},
{'teacher': '乙', 'name':'系統', 'hours': 3},
{'teacher': '乙', 'name':'計概', 'hours': 3},
{'teacher': '丙', 'name':'軟工', 'hours': 3},
{'teacher': '丙', 'name':'行動', 'hours': 3},
{'teacher': '丙', 'name':'網路', 'hours': 3},
{'teacher': '丁', 'name':'媒體', 'hours': 3},
{'teacher': '丁', 'name':'工數', 'hours': 3},
{'teacher': '丁', 'name':'動畫', 'hours': 3},
{'teacher': '丁', 'name':'電子', 'hours': 4},
{'teacher': '丁', 'name':'嵌入', 'hours': 3},
{'teacher': '戊', 'name':'網站', 'hours': 3},
{'teacher': '戊', 'name':'網頁', 'hours': 3},
{'teacher': '戊', 'name':'演算', 'hours': 3},
{'teacher': '戊', 'name':'結構', 'hours': 3},
{'teacher': '戊', 'name':'智慧', 'hours': 3}
]

teachers = ['甲', '乙', '丙', '丁', '戊']

rooms = ['A', 'B']

slots = [
'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17',
'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27',
'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37',
'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 'A47',
'A51', 'A52', 'A53', 'A54', 'A55', 'A56', 'A57',
'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17',
'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27',
'B31', 'B32', 'B33', 'B34', 'B35', 'B36', 'B37',
'B41', 'B42', 'B43', 'B44', 'B45', 'B46', 'B47',
'B51', 'B52', 'B53', 'B54', 'B55', 'B56', 'B57',
]

def hillClimbing(x, height, neighbor, max_fail=10000):
      fail = 0     #初始化
      while True:
          nx = neighbor(x) #隨機選取課程
          if height(nx)>height(x): #如果分數比較高就更新當前狀態
              x = nx
              fail = 0 #成功找到更好的分數，重置失敗計數器
          else:
              fail += 1 #分數不如當前，增加失敗計數器
              if fail > max_fail: #當錯誤到一定次數後返回當前最佳狀態 x
                  return x
      
class SolutionScheduling:
    
    def neighbor(self,x):
        change = self.v
        choose=randint(0,1) #隨機選擇0或1

        if choose == 0 :
            i=randint(0, len(slots)-1) #隨機選擇 slots 列表中的一個索引 i
            change[i]=randint(0, len(courses)-1) #是0就隨機選一個課程排入
        else :
            i=randint(0, len(slots)-1)
            j=randint(0, len(slots)-1)
            tmp=change[i] #隨機選i,j兩個做交換
            change[i]=change[j]
            change[j]=tmp
        return change
    
    
    def height(self,fills): 
        courseCounts = [0] * len(courses) #計算每門課程被安排的次數
        score = 0
        for si in range(len(slots)): #遍歷所有slots
            courseCounts[fills[si]] += 1 #計算每門課程被安排的次數
             # 如果當前課程和下一個課程相同且不是週末或中午，則增加分數
            if si < len(slots)-1 and fills[si] == fills[si+1] and si%7 != 6 and si%7 != 3:
                score += 0.1
            if si % 7 == 0 and fills[si] != 0:  # 如果課程在早上 8:00 安排，則減少分數
                score -= 0.12
        # 遍歷所有課程
        for ci in range(len(courses)):
            if (courses[ci]['hours'] >= 0): # 如果課程的總時數為非負數，則計算實際安排時數與預期時數的差異並減少分數
                score -= abs(courseCounts[ci] - courses[ci]['hours']) # 課程總時數不對
        return score
   
    def str(self): 
        outs = [] # 初始化一個空列表 outs，用於存儲輸出的字串
        fills = self.v # 獲取當前課程安排的狀態
        for i in range(len(slots)): # 遍歷所有slots
            c = courses[fills[i]]# 根據當前插槽的課程索引獲取對應的課程
            if i%7 == 0:# 每當到達一週的第一天（假設一週有七天），插入一個換行符號
                outs.append('\n')
            outs.append(slots[i] + ':' + c['name'])# 將插槽編號和對應的課程名稱組合成字串並添加到 outs 列表
        return 'height={:f} {:s}\n\n'.format(self.height(self.v), ' '.join(outs)) # 將所有插槽信息組合成一個字串，並加上計算出的評估分數
    

    def __init__(self):
        self.v = [ randint(0, len(courses)-1) for i in range(len(slots))] #隨機排課
        print("Initial schedule:", self.v) # 輸出初始課程安排
        print("Initial height:", self.height(self.v))# 評估分數
        print("Initial solution:", self.str())# 輸出初始的解決方案的字串表示
        final_solution = hillClimbing(self.v, self.height, self.neighbor) #使用爬山演算法去找更好的課程
        print("Final solution:", final_solution)   # 輸出最終找到的解決方案
        print("Final height:", self.height(final_solution)) # 計算並輸出最終解決方案的評估分數
        print("Final solution:", self.str())    # 輸出最終解決方案的字串表示

    

SolutionScheduling()#執行上述流程