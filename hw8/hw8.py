import gymnasium as gym  # 導入 gymnasium 模組，並命名為 gym
env = gym.make("CartPole-v1", render_mode="human")  # 建立 "CartPole-v1" 環境，設置 render_mode 為 "human" 以便顯示圖形

# 重置環境並獲取初始觀察值和其他資訊，種子設置為 42 保證結果可重現
observation, info = env.reset(seed=42)
score = 0  # 初始化分數為 0

# 定義一個根據觀察值決定動作的函數
def action(observation):
    if observation[3] > 0:  # 如果第 4 個觀察值（杆子的角速度）大於 0
        action = 1  # 動作設置為 1（向右移動）
    else:
        action = 0  # 否則動作設置為 0（向左移動）
    return action  # 返回決定的動作

# 進行 1000 次迭代
for _ in range(1000):
   env.render()  # 渲染當前環境
   observation, reward, terminated, truncated, info = env.step(action(observation))  # 執行動作，更新觀察值、獎勵、終止和截斷標誌及其他資訊

   score += reward  # 累加獎勵到分數
   if terminated or truncated:  # 如果環境終止或截斷
      observation, info = env.reset()  # 重置環境並獲取新的初始觀察值和其他資訊
      print('done, score=', score)  # 輸出分數
      score = 0  # 重置分數為 0
env.close()  # 關閉環境