# Make dummy data

from sklearn.linear_model import LinearRegression
import numpy as np

X = np.random.randn(500, 4)
y = X.sum(axis = 1)
print(y)

np.savetxt('X.csv', X, delimiter= ',')
np.savetxt('y.csv', y, delimiter=',')

model = LinearRegression()
model.fit(X, y)

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
initial_type = [("input", FloatTensorType(None, X.shape))]
onnx = convert_sklearn(model, name = "regression", initial_types = initial_type)
with open("simple_reg.onnx", "wb") as f:
    f.write(onnx.SerializeToString())





