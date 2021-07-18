from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten
import keras.initializers


initializer = keras.initializers.HeNormal()


model = Sequential()
model.add(Conv2D(32, kernel_size=7, kernel_initializer=initializer, activation='relu', input_shape=(150, 150, 3)))
model.add(MaxPool2D(2, 2))
model.add(Conv2D(64, kernel_size=5, kernel_initializer=initializer,  activation='relu'))
model.add(MaxPool2D(2, 2))
model.add(Conv2D(128, kernel_size=3, kernel_initializer=initializer, activation='relu'))
model.add(Flatten())
model.add(Dense(101, activation='softmax'))

# 13.) Model Summary
print(model.summary())


