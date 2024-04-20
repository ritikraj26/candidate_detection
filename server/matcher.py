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


import numpy as np
from scipy.spatial.distance import cosine
from models import Profile

def find_matching_profiles(image_vector):
    # Load all profiles from the database
    all_profiles = Profile.query.all()
    best_match = None
    min_distance = float('inf')

    for profile in all_profiles:
        profile_vector = profile.facial_encoding
        distance = cosine(profile_vector, image_vector)
        if distance < min_distance:
            min_distance = distance
            best_match = profile

    if best_match:
        return {'name': best_match.name, 'organization': best_match.organization, 'linkedin_url': best_match.linkedin_url}
    else:
        return None
