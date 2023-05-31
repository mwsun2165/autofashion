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

train_df = pd.read_csv("/work/Fashion MNIST/fashion-mnist_train.csv")
train_data = np.array(train_df, dtype = 'float32')
test_df = pd.read_csv("/work/Fashion MNIST/fashion-mnist_test.csv")
test_data = np.array(test_df, dtype = 'float32')

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

x_train = train_data[:, 1:] / 255
y_train = train_data[:, 0]
x_test = test_data[:, 1:] / 255
y_test = test_data[:, 0]
image_shape = (28, 28, 1)

x_train, x_validate, y_train, y_validate = train_test_split(x_train, y_train, test_size = 0.2)
x_train = x_train.reshape(x_train.shape[0],*image_shape)
x_test = x_test.reshape(x_test.shape[0],*image_shape)
x_validate = x_validate.reshape(x_validate.shape[0],*image_shape)

model = keras.Sequential()
model.add(Conv2D(filters=32,kernel_size=3,activation='relu',input_shape = image_shape))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(32,activation='relu'))
model.add(Dense(10,activation = 'softmax'))
model.compile(loss ='sparse_categorical_crossentropy', optimizer=Adam(learning_rate=0.005), metrics =['accuracy'])
model.fit(x_train, y_train, batch_size = batch_size, epochs = epochs, validation_data=(x_validate, y_validate))
model.save("kerasModel.json")
testm = model.evaluate(x=x_test, y=y_test)
print(testm[0])
print(testm[1])