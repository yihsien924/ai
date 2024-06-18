import torch  # 導入 PyTorch 庫
import torch.nn as nn  # 導入 PyTorch 的神經網路模組
import torch.nn.functional as F  # 導入 PyTorch 的函數庫，包含激活函數等

# 定義一個神經網路類別，繼承自 nn.Module
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()  # 初始化父類別
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5)  # 定義第一個卷積層，輸入通道數為 1，輸出通道數為 16，卷積核大小為 5
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5)  # 定義第二個卷積層，輸入通道數為 16，輸出通道數為 32，卷積核大小為 5
        self.fc1 = nn.Linear(32 * 4 * 4, 50)  # 定義第一個全連接層，輸入大小為 32*4*4，輸出大小為 50
        self.fc2 = nn.Linear(50, 10)  # 定義第二個全連接層，輸入大小為 50，輸出大小為 10（對應 10 個分類）

    # 定義前向傳播函數
    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))  # 對第一個卷積層的輸出進行 ReLU 激活函數和 2x2 最大池化
        x = F.relu(F.max_pool2d(self.conv2(x), 2))  # 對第二個卷積層的輸出進行 ReLU 激活函數和 2x2 最大池化
        x = x.view(-1, 32 * 4 * 4)  # 將張量展平為一維，大小為 32*4*4
        x = F.relu(self.fc1(x))  # 對第一個全連接層的輸出進行 ReLU 激活函數
        x = F.dropout(x, training=self.training)  # 在訓練期間應用 Dropout，防止過擬合
        x = self.fc2(x)  # 計算最終輸出
        return x  # 返回輸出