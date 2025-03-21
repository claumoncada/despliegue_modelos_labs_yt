import os
from flask import Flask, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename
from transformers import AutoProcessor, AutoModelForImageTextToText, AutoImageProcessor, AutoModelForImageClassification
import torch

app = Flask(__name__)

# guardar las fotos subidas
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cargar modelos 
print("Iniciando carga de modelos...")
caption_processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base", local_files_only=False)
caption_model = AutoModelForImageTextToText.from_pretrained("Salesforce/blip-image-captioning-base", local_files_only=False)
tags_processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224", local_files_only=False)
tags_model = AutoModelForImageClassification.from_pretrained("google/vit-base-patch16-224", local_files_only=False)
tags_model.eval()
print("Modelos cargados exitosamente")


@app.route('/', methods=['GET', 'POST'])
def upload_photo():
    if request.method == 'POST':
        # Procesar la imagen 
        photo = request.files['photo']
        if photo:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)

            # Procesar la imagen con el modelo de Image Captioning
            image = Image.open(photo_path).convert("RGB")
            caption_inputs = caption_processor(images=image, return_tensors="pt")
            caption_outputs = caption_model.generate(**caption_inputs)
            description = caption_processor.batch_decode(caption_outputs, skip_special_tokens=True)[0]
            print(f"Descripción generada: {description}")

            # Procesar la imagen con el modelo de clasificación (tags)
            tag_inputs = tags_processor(images=image, return_tensors="pt")
            tag_outputs = tags_model(**tag_inputs)
            logits = tag_outputs.logits
            predicted_ids = torch.argsort(logits, dim=-1, descending=True)[0][:5]  # Top 5 tags
            tags = [tags_model.config.id2label[idx.item()] for idx in predicted_ids]
            print(f"Tags generados: {tags}")

            # mostrar resultados
            return render_template('result.html',
                                   photo_url=photo_path,
                                   description=description,
                                   tags=tags)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)  