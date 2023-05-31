import PIL
from PIL import Image, ImageOps
import tensorflow as tf
import pandas as pd
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Dense,Flatten,Dropout
from keras.optimizers import Adam
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

num_classes = 10
epochs = 100
batch_size = 4096

cloth_type = { #label
    0: "T-shirt/top",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Boot"
}
# converting image to 28x28
def convImg(path): #/work/Fashion MNIST/name.jpg
    gimg = ImageOps.grayscale(Image.open(path))
    ow, oh = gimg.size
    tupp = ((int(ow/2-oh/2), 0, int(ow/2+oh/2), oh), (0, int(oh/2+ow/2), ow, int(oh/2-ow/2)))[oh > ow]
    cr = gimg.crop(tupp)
    ret = cr.resize((28, 28))
    ret.save("/work/Fashion MNIST/lastimg.jpg")
    return np.array(ret, dtype = 'float32')
def convImg2(path): #/work/Fashion MNIST/name.jpg
    gimg = ImageOps.grayscale(Image.open(path))
    ow, oh = gimg.size
    ret = gimg.resize((28, 28))
    ret.save("/work/Fashion MNIST/lastimg.jpg")
    return np.array(ret, dtype = 'float32')

convImg2("/work/tempyyy.jpg")

def printResult(x): print(cloth_type[np.where(pred[0] == 1.)[0][0]])

model = keras.models.load_model("kerasModel.json")
image = Image.open("/work/Fashion MNIST/lastimg.jpg")
px = image.load()
val = [px[x, y] for y in range(image.size[1]) for x in range(image.size[0])]
im = np.array(val, dtype = 'float32')
im = im.reshape((1, 28, 28))
pred = model.predict(im)
# print(np.where(pred[0] == 1.)[0][0])
printResult(pred)