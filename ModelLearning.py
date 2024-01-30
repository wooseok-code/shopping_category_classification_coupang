import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import *
from tensorflow.keras.layers import *

# X_train, X_test, Y_train, Y_test = np.load(    './news_data_max_27_wordsize_3885.npy', allow_pickle=True)
X_train, X_test, Y_train, Y_test = np.load(    './last_29_wordsize_16995.npy', allow_pickle=True)

print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

model = Sequential()
model.add(Embedding(16995, 300, input_length=29))
# model.add(Embedding(3885, 300, input_length=27))
model.add(Conv1D(32, kernel_size=5, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=1))
model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(5, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=128, epochs=10, validation_data=(X_test, Y_test))
# model.save('./models/coupang_classification_model_{}.h5'.format(fit_hist.history['val_accuracy'][-1]))
model.save('./models/last_classification_model_{}.h5'.format(fit_hist.history['val_accuracy'][-1]))
plt.plot(fit_hist.history['val_accuracy'], label='validation accuracy')
plt.plot(fit_hist.history['accuracy'], label='train accuracy')
plt.legend()
plt.show()