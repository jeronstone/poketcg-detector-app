from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
from generate_tensors import load_tensors
import json
from index import get_prediction

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"  # Folder to store uploaded images
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

data, pths, vectorizer, matrix = load_tensors(finame='coopertest_sv6')

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)  # Save the uploaded image

    # Process the image with your Python script
    return jsonify({'message': 'Image uploaded successfully', 'image_path': image_path})

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Run the Python script (e.g., script.py)
        data = request.json  # Get JSON data from JS request
        arg = data.get('argument', '')  # Extract argument, default to empty string

        print(f'got {data} and {arg}')
        '''
        # Run Python script with the argument
        result = subprocess.run(['python3', 'index.py', arg], capture_output=True, text=True)
        print(result.stdout)
        result = json.loads(result.stdout)
        ret = jsonify({"pname": result["pname"], "set":  result["set"], "score": result["score"], "price":  result["price"], "imagelink":  result["imagelink"]})
        print(ret)
        return ret
        '''
        result = get_prediction(arg, data, pths, vectorizer, matrix)
        result = json.loads(result)
        ret = jsonify({"pname": result["pname"], "set":  result["set"], "score": result["score"], "price":  result["price"], "imagelink":  result["imagelink"], "time":  result["time"]})
        print(ret)
        return ret
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
