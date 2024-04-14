from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from PIL import Image

app = Flask(__name__)
CORS(app)

# Load the TensorFlow model
model = load_model("fish_cnn.h5")  # Replace with the correct path

# Function to preprocess an image for prediction
def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Rescale to [0, 1]
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        # Save the uploaded image temporarily (you may need to handle this differently in production)
        temp_image_path = "temp_image.jpg"
        file.save(temp_image_path)

        # Preprocess the image for prediction
        preprocessed_image = preprocess_image(temp_image_path)

        # Make predictions
        predictions = model.predict(preprocessed_image)

        # Get the predicted class index
        predicted_class_index = np.argmax(predictions[0])
        class_labels =  ['Coral','Jelly Fish','Lobster','Penguin','Seal','Sharks','Squid','Turtle']
        class_label = class_labels[predicted_class_index]
        confidence = float(predictions[0][predicted_class_index])

        # Remove the temporary image file
        os.remove(temp_image_path)

        return jsonify({'class_label': class_label, 'confidence': confidence})

    except Exception as e:
        # Log the exception to a file or another logging mechanism
        with open("error.log", "a") as log_file:
            log_file.write(f"An error occurred: {str(e)}\n")
        # Return an error response
        return jsonify({'error': 'An internal server error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
