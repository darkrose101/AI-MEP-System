import tensorflow as tf
import pandas as pd
import numpy as np
import warnings
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


warnings.filterwarnings("ignore", category=FutureWarning)

data1 = pd.read_csv('sample_data.csv')
data1 = data1.drop(columns=['Date'])

X = data1.drop(columns=['Name', 'Email', 'Absent'])
y = data1.iloc[:, -1].values


# Encoding categorical features using one-hot encoding
categorical_cols = ['Department']
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), categorical_cols)], remainder='passthrough')
X = np.array(ct.fit_transform(X))


# Splitting the dataset into training and test set
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)



bobby = tf.keras.models.Sequential()

# Adding input layer with 8 neurons (features)
bobby.add(tf.keras.layers.Dense(units=64, activation='relu'))

bobby.add(tf.keras.layers.Dense(units=64, activation='relu'))
bobby.add(tf.keras.layers.Dense(units=64, activation='relu'))
bobby.add(tf.keras.layers.Dense(units=64, activation='relu'))

bobby.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

#Compiling the networks
bobby.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#Training the young brains
bobby.fit(x_train, y_train, epochs=500)

bobby.evaluate(x_test, y_test)

bobby.save('model/model1')


#################################################################################################
#################################################################################################