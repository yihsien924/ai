import random #初始化
citys = [
    (0,3),(0,0),
    (0,2),(0,1),
    (1,0),(1,3),
    (2,0),(2,3),
    (3,0),(3,3),
    (3,1),(3,2)
]

#計算兩點間的距離
def distance(p1, p2):
    x1, y1 = p1# 從 p1 中解包出座標值 x1 和 y1
    x2, y2 = p2# 從 p2 中解包出座標值 x2 和 y2

    return ((x2-x1)**2+(y2-y1)**2)**0.5# 計算兩點之間的距離並返回結果

#計算總距離
def pathLength(p):
    dist = 0# 初始化距離總和為 0
    plen = len(p) # 獲取路徑 p 的長度
    for i in range(plen):# 累加從 p[i] 到 p[(i+1)%plen] 兩點之間的距離，這裡使用了 %plen 確保循環計算
        dist += distance(citys[p[i]], citys[p[(i+1)%plen]])
    return dist


l = len(citys)# 獲取城市列表 citys 的長度
path = [(i+1)%l for i in range(l)]# 創建一個包含每個城市索引的路徑，索引從 1 到 l，循環到 0
print(path)
print('pathLength=', pathLength(path))# 輸出計算得到的路徑長度


#隨機兩個做交換
def neighbor(p):
    p2 = p.copy()# 複製路徑 p，以避免修改原始路徑
    ran = len(p2)# 獲取路徑的長度
    city1 = random.randint(0, ran-1)# 隨機選擇第一個城市索引
    city2 = random.randint(0, ran-1)# 隨機選擇第二個城市索引
    temp = p2[city1]# 將第一個城市的索引暫存到 temp 中
    p2[city1] = p2[city2]# 將第二個城市的索引值賦給第一個城市
    p2[city2] = temp# 將暫存的第一個城市索引賦給第二個城市
    return p2# 返回生成的鄰近路徑
    
    
def hillClimbing(x,pathLength, neighbor,max_fail=10000):
    fail = 0
    while True:
        nx = neighbor(x) # 生成 x 的一個鄰近解 nx
        if pathLength(nx) < pathLength(x) and pathLength(nx) != 0:# 如果 nx 的路徑長度比 x 小且不為零
            x = nx# 接受 nx 作為新的解 x
            fail = 0# 重置失敗計數器
        else:
            fail += 1
            if fail > max_fail: # 如果失敗計數超過設定的最大失敗次數
                return x
result = pathLength(hillClimbing(path,pathLength,neighbor))# 使用爬山演算法尋找最佳路徑，並計算最終路徑長度
print('path=',hillClimbing(path,pathLength,neighbor)) #輸出找到的最佳路徑
print('pathLength=', result)# 輸出最佳路徑的長度