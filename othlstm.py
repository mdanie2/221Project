from keras.preprocessing import sequence 
from keras.models import Sequential 
from keras.layers import Dense, Dropout, Embedding, LSTM 
from keras.datasets import imdb 

num_words = 1000 
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=num_words) 

X_train = sequence.pad_sequences(X_train, maxlen=200) 
X_test = sequence.pad_sequences(X_test, maxlen=200)

model = Sequential() 
model.add(Embedding(num_words, 50, input_length=200)) 
model.add(Dropout(0.2)) 
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2)) 
model.add(Dense(250, activation='relu')) 
model.add(Dropout(0.2)) 
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) 

model.fit(X_train, y_train, batch_size=64, epochs=5) 

print('\nAccuracy: {}'. format(model.evaluate(X_test, y_test)[1]))