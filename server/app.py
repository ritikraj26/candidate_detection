from flask import Flask, jsonify, request
import os
import werkzeug
from flask_cors import CORS

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello from Flask!'})


@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'})

    image_file = request.files['image']
    print(image_file)
    if image_file.filename == '':
        return jsonify({'error': 'No selected image'})

    # if image_file and werkzeug.utils.secure_filename(image_file.filename):
    #     filename = werkzeug.utils.secure_filename(image_file.filename)
    #     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #     image_file.save(filepath)
    #     return jsonify({'message': 'Image uploaded!'})
    if image_file:
        filename = image_file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        return jsonify({'message': 'Image uploaded!'})
    else:
        return jsonify({'error': 'Invalid image file'})

if __name__ == '__main__':
    app.run(debug=True)
