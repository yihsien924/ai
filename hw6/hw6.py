# 來源 -- https://github.com/newcodevelop/micrograd/blob/master/micrograd/engine.py
# 有參考老師 https://github.com/ccc112b/py2gpt/blob/master/03b-MacroGrad/macrograd/engine.py
# 推薦網頁https://r23456999.medium.com/%E4%BD%95%E8%AC%82-cross-entropy-%E4%BA%A4%E5%8F%89%E7%86%B5-b6d4cef9189d
import numpy as np

class Tensor:
    def __init__(self, data, _children=(), _op=''):
        # 初始化數據和梯度
        self.data = np.array(data)
        self.grad = np.zeros(self.data.shape)
        # 用於自動求導圖構建的內部變量
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op  # 生成此節點的操作，用於調試等

    @property
    def shape(self):
        return self.data.shape
    
    def __add__(self, other):
        # 進行加法操作
        other = other if isinstance(other, Tensor) else Tensor(np.zeros(self.shape) + other)  # 保持維度一致
        out = Tensor(self.data + other.data, (self, other), '+')

        def _backward():
            # 定義反向傳播
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out

    def __mul__(self, other):
        # 進行乘法操作
        other = other if isinstance(other, Tensor) else Tensor(np.zeros(self.shape) + other)  # 保持維度一致
        out = Tensor(self.data * other.data, (self, other), '*')

        def _backward():
            # 定義反向傳播
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward

        return out

    def __pow__(self, other):
        # 指數運算，只支持整數和浮點數
        assert isinstance(other, (int, float)), "目前只支持整數/浮點數的指數"
        out = Tensor(self.data**other, (self,), f'**{other}')

        def _backward():
            # 定義反向傳播
            self.grad += (other * self.data**(other-1)) * out.grad
        out._backward = _backward

        return out

    def relu(self):
        # ReLU 激活函數
        out = Tensor(np.maximum(0, self.data), (self,), 'relu')

        def _backward():
            # 定義反向傳播
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward

        return out

    def matmul(self, other):
        # 矩陣乘法
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(np.matmul(self.data, other.data), (self, other), 'matmul')

        def _backward():
            # 定義反向傳播
            self.grad += np.dot(out.grad, other.data.T)
            other.grad += np.dot(self.data.T, out.grad)
        out._backward = _backward

        return out

    def softmax(self):
        # Softmax 激活函數
        out = Tensor(np.exp(self.data) / np.sum(np.exp(self.data), axis=1)[:, None], (self,), 'softmax')
        softmax = out.data

        def _backward():
            # 定義反向傳播
            s = np.sum(out.grad * softmax, 1)
            t = np.reshape(s, [-1, 1])  # reshape 為 n*1
            self.grad += (out.grad - t) * softmax
        out._backward = _backward

        return out

    def log(self):
        # 對數運算
        out = Tensor(np.log(self.data), (self,), 'log')

        def _backward():
            # 定義反向傳播
            self.grad += out.grad / self.data
        out._backward = _backward

        return out    
    
    def sum(self, axis=None):
        # 求和操作
        out = Tensor(np.sum(self.data, axis=axis), (self,), 'SUM')

        def _backward():
            # 定義反向傳播
            output_shape = np.array(self.data.shape)
            output_shape[axis] = 1
            tile_scaling = self.data.shape // output_shape
            grad = np.reshape(out.grad, output_shape)
            self.grad += np.tile(grad, tile_scaling)
        out._backward = _backward

        return out

    def cross_entropy(self, yb):
        # 交叉熵損失函數
        log = self.log()
        zb = yb * log
        out = zb.sum(axis=1)
        ans = -out.sum()
        return ans 

    def backward(self):
        # 自動求導，構建拓撲排序
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        # 應用鏈式法則計算梯度
        self.grad = 1
        for v in reversed(topo):
            v._backward()

    def __neg__(self):
        # 負號運算
        return self * -1

    def __radd__(self, other):
        # 右加法
        return self + other

    def __sub__(self, other):
        # 減法
        return self + (-other)

    def __rsub__(self, other):
        # 右減法
        return other + (-self)

    def __rmul__(self, other):
        # 右乘法
        return self * other

    def __truediv__(self, other):
        # 除法
        return self * other**-1

    def __rtruediv__(self, other):
        # 右除法
        return other * self**-1

    def __repr__(self):
        # 打印 Tensor 的表示
        return f"Tensor(data={self.data}, grad={self.grad})"