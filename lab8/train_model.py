# This file is designed based on MlFlow tutorial
# https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html

import mlflow
from mlflow.models import infer_signature

from utility import pipeline

# TODO: Set the MLFlow tracking server uri
uri = "http://127.0.0.1:6001"  # El URI del servidor MLFlow (asegúrate de que sea el correcto)
# Use mlflow.set_tracking_uri to set the uri
mlflow.set_tracking_uri(uri)

# Set experiment name
email = "claudia1605ve@gmail.com"  # TODO: Reemplaza con tu correo electrónico
experiment_name = f"{email}-lab8"  # Asegúrate de que el nombre del experimento sea adecuado
mlflow.set_experiment(experiment_name)

# TODO: Generate train and test dataset using `pipeline.data_preprocessing` function
X_train, X_test, y_train, y_test = pipeline.data_preprocessing()

params = {
    "solver": "lbfgs",
    "max_iter": 1000,
    "multi_class": "auto",
    "random_state": 8888,
}

# TODO: Use `pipeline.train_logistic_regression` to generate trained model
trained_model = pipeline.train_logistic_regression(X_train, y_train, params)

# TODO: Use `pipeline.evaluation` to evaluate the model
accuracy = pipeline.evaluation(trained_model, X_test, y_test)

# Log model and metrics to tracking server
# Start an MLflow run
run_name = None  # You can specify a run name or let MLFlow choose one for you.
with mlflow.start_run(run_name=run_name):
    mlflow.log_params(params)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.set_tag("Training Info", "Basic LR model for digits_model data")
    # Infer the model signature
    signature = infer_signature(X_train, trained_model.predict(X_train))
    # Log the model
    model_info = mlflow.sklearn.log_model(
        sk_model=trained_model,
        artifact_path="models",  # El path del artifact que puede ser adecuado
        signature=signature,
        input_example=X_train,
        registered_model_name=pipeline.generate_model_name(),  # Opcional: Reemplaza con un nombre estático si es necesario
    )