# Copyright 2024 ritik
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Blueprint
import requests
from video_processing import start_video_processing, handle_motion
from image_processing import detect_faces
from scraper import process_image
from matcher import find_matching_profiles

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/start-monitoring', methods=['GET'])
def start_monitoring():
    start_video_processing(handle_motion)
    return 'Monitoring Started!', 200

@app_routes.route('/process-image', methods=['POST'])
def start_processing():
    if 'image' not in request.files:
        return 'No image found in request!', 400

    image_file = request.files['image']
    image_data = image_file.read()

    try:
        faces = detect_faces(image_data)
        if not faces:
                return jsonify({'success': False, 'message': 'No faces found in the image.'}), 400 
        face_vector = process_image(image_data)
        profiles = find_matching_profiles(face_vector)
        return jsonify({'success': True, 'profiles': profiles}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500