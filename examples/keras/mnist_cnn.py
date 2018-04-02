#!/usr/bin/env python

from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Input, Dense, Dropout, Flatten, GlobalAveragePooling2D
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.models import Model


def main(architecture_parameters):
  batch_size = 1280
  num_classes = 10
  epochs = 1
  img_rows, img_cols = 28, 28

  (x_train, y_train), (x_test, y_test) = mnist.load_data()
  x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
  x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
  x_train = x_train.astype('float32')
  x_test = x_test.astype('float32')
  x_train /= 255
  x_test /= 255
  print('x_train shape:', x_train.shape)
  print(x_train.shape[0], 'train samples')
  print(x_test.shape[0], 'test samples')

  # convert class vectors to binary class matrices
  y_train = keras.utils.to_categorical(y_train, num_classes)
  y_test = keras.utils.to_categorical(y_test, num_classes)

  # model = build_model()
  # architecture_parameters = [32, 3, 2, 64, 3, 2]
  model = build_model_with_architecture(architecture_parameters)

  model.compile(
      loss=keras.losses.categorical_crossentropy,
      optimizer=keras.optimizers.Adadelta(),
      metrics=['accuracy'])

  model.fit(
      x_train,
      y_train,
      batch_size=batch_size,
      epochs=epochs,
      verbose=1,
      validation_data=(x_test, y_test))
  score = model.evaluate(x_test, y_test, verbose=0)
  print('Test loss:', score[0])
  print('Test accuracy:', score[1])

  return score[1]


def build_model():
  img_rows, img_cols = 28, 28
  input_shape = (img_rows, img_cols, 1)
  num_classes = 10

  model = Sequential()
  model.add(
      Conv2D(
          32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Conv2D(64, (3, 3), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Flatten())
  model.add(Dense(num_classes, activation='softmax'))

  return model


def build_model_with_architecture(architecture_parameters):
  # [filter_number, convolution_kernel_size, max_polling_size]
  # Example: architecture_parameters = [32, 3, 2, 64, 3, 2]

  img_rows, img_cols = 28, 28
  input_shape = (img_rows, img_cols, 1)
  num_classes = 10

  layer_number = int(len(architecture_parameters) / 3)

  model = Sequential()
  for layer_index in range(layer_number):
    filter_number = architecture_parameters[0 + layer_index * 3]
    convolution_kernel_size = architecture_parameters[1 + layer_index * 3]
    max_polling_size = architecture_parameters[2 + layer_index * 3]

    if layer_index == 0:
      model.add(
          Conv2D(
              filter_number,
              kernel_size=(convolution_kernel_size, convolution_kernel_size),
              activation='relu',
              input_shape=input_shape))
    else:
      model.add(
          Conv2D(
              filter_number,
              kernel_size=(convolution_kernel_size, convolution_kernel_size),
              activation='relu'))
    model.add(MaxPooling2D(pool_size=(max_polling_size, max_polling_size)))

  model.add(Flatten())
  model.add(Dense(num_classes, activation='softmax'))
  return model


def train(**kwargs):
  # Convert json arguments to the architecture list
  architecture_parameters = []

  layer_number = int(len(kwargs) / 3)
  for layer_index in range(layer_number):
    for i in range(3):
      if i == 0:
        key_string = "filter_number" + str(layer_index)
      elif i == 1:
        key_string = "convolution_kernel_size" + str(layer_index)
      elif i == 2:
        key_string = "max_polling_size" + str(layer_index)

      architecture_parameters.append(kwargs.get(key_string))

  return main(architecture_parameters)


if __name__ == "__main__":
  #main([])

  import keras_util
  keras_util.main(train)
