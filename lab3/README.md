# Lab 3: Building an ML-enabled Product

Este laboratorio tiene como objetivo implementar técnicas de machine learning mediante el uso de una aplicación web.

## Modelos de Machine Learning
Se han utilizado los siguientes modelos preentrenados para realizar las tareas de descripción y tagging de objetos:
- `Salesforce/blip-image-captioning-base`: Modelo de visión computacional para generar descripciones automáticas de imágenes (texto alternativo).
- `google/vit-base-patch16-224`: Modelo basado en Vision Transformer (ViT) para identificar objetos dentro de las imágenes.

## Características
- Los usuarios pueden cargar imágenes y generar automáticamente una descripción y tags para la misma.

## Despliegue de la Aplicación
1. Clonar este repositorio `https://github.com/claumoncada/despliegue_modelos_labs_yt.git`
2. Instalar las dependencias necesarias.
3. Ejecuta la aplicación Flask `app.py`.

Se despliega la siguiente página donde el usuario tiene la posibilidad de subir la imagen que desea procesar. Al seleccionar el botón Generar Descripción y Tags inicia el proceso de análisis.

<img src="lab3/images_rd/upload_image.png">

Luego, se despliega la siguiente página con los resultados:

<img src="lab3/images_rd/results_lab2.png">

Aquí se muestra la imagen subida con su respectiva descripción y tags generados por los modelos mencionados para cada funcionalidad. Para reiniciar el proceso, el usuario puede seleccionar el botón Subir otra foto y procesar las imágenes que considere necesarias. 

