import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from utility import pipeline
from sklearn.svm import SVC  # Importar el modelo SVM
from sklearn.model_selection import train_test_split

# TODO: Set the MLFlow tracking server URI
uri = "http://127.0.0.1:6001"  # Usando la URL local de MLFlow
mlflow.set_tracking_uri(uri)

# Set experiment name
email = "claudia1605ve@gmail.com"  # Cambia este email por el tuyo
experiment_name = f"{email}-lab8"
mlflow.set_experiment(experiment_name)

# TODO: Generate train and test datasets using `pipeline.data_preprocessing` function
X_train, X_test, y_train, y_test = pipeline.data_preprocessing()

# Parámetros para el modelo SVM
params = {
    "C": 1.0,
    "kernel": "linear",  # Puedes probar con diferentes kernels, como "rbf", "poly", etc.
    "random_state": 8888,
}

# Entrenamiento del modelo SVM
model = SVC(C=params["C"], kernel=params["kernel"], random_state=params["random_state"])
model.fit(X_train, y_train)

# TODO: Use `pipeline.evaluation` to evaluate the model
accuracy = pipeline.evaluation(model, X_test, y_test)

# Log model and metrics to the tracking server
# Start an MLflow run
run_name = None  # Puedes especificar un nombre para la ejecución o dejar que MLFlow elija uno por ti
with mlflow.start_run(run_name=run_name):
    # Log params, metrics, and model information
    mlflow.log_params(params)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.set_tag("Training Info", "SVM model for digits_model data")

    # Infer the model signature
    signature = infer_signature(X_train, model.predict(X_train))
    
    # Log the model and register it
    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="models",
        signature=signature,
        input_example=X_train,
        registered_model_name="iris_model"  # Nombre del modelo registrado
    )

    #print(f"Modelo registrado como nueva versión: {model_info.name} - Versión: {model_info.version}")