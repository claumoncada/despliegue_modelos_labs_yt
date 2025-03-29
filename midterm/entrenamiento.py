import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, precision_score, mean_squared_error
import pickle
import time

# Datos: https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset?select=movie.csv
# Cargar datos
ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')

# cada fila representa a un usuario, cada columna a una película, y el valor es la calificación que ese usuario le dio a esa película.
# filas representan a los usuarios (userId) y las columnas representan las películas (movieId).
user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
X = user_item_matrix.values

# Crear conjuntos de entrenamiento y prueba
train_data, test_data = train_test_split(ratings, test_size=0.2, random_state=42)
X_train = train_data[['userId', 'movieId']].values  # Dos características
y_train = train_data['rating'].values
X_test = test_data[['userId', 'movieId']].values
y_test = test_data['rating'].values

# Diccionario para guardar métricas
metrics = {}

# Modelo KNN
# el modelo predice la calificación de una película basada en las 5 calificaciones más cercanas.
start_time = time.time()
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train, y_train)
knn_training_time = time.time() - start_time
print(f"Tiempo de entrenamiento para KNN (regresión): {knn_training_time} segundos")

# Predicciones para KNN
knn_predictions = knn.predict(X_test)
knn_mse = mean_squared_error(y_test, knn_predictions)
print(f"MSE para KNN: {knn_mse}")
metrics['knn_training_time'] = knn_training_time
metrics['knn_mse'] = knn_mse

# Modelo de Regresión Lineal
start_time = time.time()
reg = LinearRegression()
reg.fit(X_train, y_train)
reg_training_time = time.time() - start_time
print(f"Tiempo de entrenamiento para Regresión Lineal: {reg_training_time} segundos")

# Predicciones para Regresión Lineal
reg_predictions = reg.predict(X_test)
reg_mse = mean_squared_error(y_test, reg_predictions)
print(f"MSE para Regresión Lineal: {reg_mse}")
metrics['reg_training_time'] = reg_training_time
metrics['reg_mse'] = reg_mse

# Guardar métricas en archivo
#with open('models/metrics.pkl', 'wb') as f:
#    pickle.dump(metrics, f)

# Guardar modelos
with open('models/knn_model.pkl', 'wb') as f:
    pickle.dump(knn, f)

with open('models/reg_model.pkl', 'wb') as f:
    pickle.dump(reg, f)

print("Modelos entrenados y guardados con métricas.")

