# pipeline_entrenamiento_modelo.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
import time
import os
import csv
from prefect import task, flow

# Directorio para guardar los resultados
RESULTADOS_DIR = 'resultados_entrenamiento'
if not os.path.exists(RESULTADOS_DIR):
    os.makedirs(RESULTADOS_DIR)

# Cargar datos
@task
def cargar_datos():
    ratings = pd.read_csv('datasets/ratings.csv')
    movies = pd.read_csv('datasets/movies.csv')
    return ratings, movies

# Preprocesamiento de datos
@task
def preprocesar_datos(ratings):
    user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
    X = user_item_matrix.values
    train_data, test_data = train_test_split(ratings, test_size=0.2, random_state=42)
    X_train = train_data[['userId', 'movieId']].values  # Dos características
    y_train = train_data['rating'].values
    X_test = test_data[['userId', 'movieId']].values
    y_test = test_data['rating'].values
    return X_train, y_train, X_test, y_test

# Entrenamiento y evaluación del modelo KNN
@task
def entrenar_knn(X_train, y_train, X_test, y_test):
    start_time = time.time()
    knn = KNeighborsRegressor(n_neighbors=5)
    knn.fit(X_train, y_train)
    knn_training_time = time.time() - start_time

    # Predicciones para KNN
    knn_predictions = knn.predict(X_test)
    knn_mse = mean_squared_error(y_test, knn_predictions)
    return knn, knn_training_time, knn_mse

# Entrenamiento y evaluación del modelo de Regresión Lineal
@task
def entrenar_regresion_lineal(X_train, y_train, X_test, y_test):
    start_time = time.time()
    reg = LinearRegression()
    reg.fit(X_train, y_train)
    reg_training_time = time.time() - start_time

    # Predicciones para Regresión Lineal
    reg_predictions = reg.predict(X_test)
    reg_mse = mean_squared_error(y_test, reg_predictions)
    return reg, reg_training_time, reg_mse

# Guardar modelos entrenados
@task
def guardar_modelos(knn, reg):
    with open(os.path.join(RESULTADOS_DIR, 'knn_model.pkl'), 'wb') as f:
        pickle.dump(knn, f)

    with open(os.path.join(RESULTADOS_DIR, 'reg_model.pkl'), 'wb') as f:
        pickle.dump(reg, f)

# Guardar métricas de entrenamiento en un archivo CSV
@task
def guardar_metricas_csv(knn_training_time, knn_mse, reg_training_time, reg_mse):
    # Definir el archivo CSV donde se guardarán las métricas
    metrics_file = os.path.join(RESULTADOS_DIR, 'metricas.csv')

    # Escribir las métricas en el archivo CSV
    with open(metrics_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Si el archivo está vacío, escribir los encabezados
        if file.tell() == 0:
            writer.writerow(['Modelo', 'Tiempo de Entrenamiento (s)', 'MSE'])
        
        # Escribir las métricas de KNN
        writer.writerow(['KNN', knn_training_time, knn_mse])
        
        # Escribir las métricas de Regresión Lineal
        writer.writerow(['Regresión Lineal', reg_training_time, reg_mse])

# Definir el flujo principal
@flow(name="Pipeline de Entrenamiento de Modelos")
def pipeline_entrenamiento():
    ratings, movies = cargar_datos()
    X_train, y_train, X_test, y_test = preprocesar_datos(ratings)
    
    knn, knn_training_time, knn_mse = entrenar_knn(X_train, y_train, X_test, y_test)
    reg, reg_training_time, reg_mse = entrenar_regresion_lineal(X_train, y_train, X_test, y_test)
    
    guardar_modelos(knn, reg)
    guardar_metricas_csv(knn_training_time, knn_mse, reg_training_time, reg_mse)

    print("Modelos entrenados y resultados guardados en la carpeta 'resultados_entrenamiento'.")

if __name__ == "__main__":
    pipeline_entrenamiento()
