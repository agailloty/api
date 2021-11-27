import skl2onnx
import onnx
import sklearn
from sklearn.linear_model import LogisticRegression
import numpy as np
import onnxruntime as rt

X = np.loadtxt("X.csv", np.float32, delimiter= ",")

sess = rt.InferenceSession("simple_reg.onnx")
input_name = sess.get_inputs()[0].name
label_name = sess.get_outputs()[0].name

print(input_name)
print(label_name)

pred_onx = sess.run(
    [label_name], {input_name: X.astype(np.float32)})[0]
print(pred_onx)