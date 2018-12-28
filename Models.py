from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras import backend as K
 
class LeNet:
	@staticmethod
	def build(width=32,height=32,depth=3,classes=10):
		model = Sequential()
		inputShape = (height, width, depth)
		if K.image_data_format() == 'channels_first': inputShape = (depth, height, width)
		model.add(Conv2D(20, (5,5), padding = "same", input_shape=inputShape, activation='relu'))
		model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
		model.add(Conv2D(50, (5, 5), padding="same"))
		model.add(Conv2D(50, (5,5), padding='same', activation='relu'))
		model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
		model.add(Flatten())
		model.add(Dense(500, activation = 'relu'))
		model.add(Dense(classes, activation = 'softmax'))
		return model

class Cifar:
    @staticmethod
    def build(width=32, height=32, depth=3, classes=10, rate=.5):
        model = Sequential()
        inputShape = (height, width, depth)
        if K.image_data_format() == 'channels_first': inputShape = (depth, height, width)
        model.add(Conv2D(30, (3,3), padding='same', input_shape=inputShape, activation='relu'))
        model.add(Conv2D(30, (3,3), padding='same', activation='relu'))
        model.add(Conv2D(30, (3,3), padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
        model.add(Dropout(rate=rate))
        model.add(Conv2D(50, (3,3), padding='same', activation='relu'))
        model.add(Conv2D(50, (3,3), padding='same', activation='relu'))
        model.add(Conv2D(50, (3,3), padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
        model.add(Dropout(rate=rate))
        model.add(Conv2D(80, (3,3), padding='same', activation='relu'))
        model.add(Conv2D(80, (3,3), padding='same', activation='relu'))
        model.add(Conv2D(80, (3,3), padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(8,8), strides=(8,8)))
        model.add(Flatten())
        model.add(Dropout(rate=rate))
        model.add(Dense(500, activation='relu'))
        model.add(Dense(classes, activation = 'softmax'))
        return model
