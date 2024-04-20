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


import requests
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
import io
from app import db
from models import Profile

def scrape_profile(urls):
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                name = soup.find('h1', class_='profile-name').text.strip()
                organization = soup.find('p', class_='profile-organization').text.strip()
                profile_image_url = soup.find('img', class_='profile-image')['src']
                image_vector = process_image(profile_image_url)
                save_to_database(name, organization, url, image_vector)
                return {'name': name, 'organization': organization, 'linkedin_url': url, 'facial_encoding': image_vector}
            else:
                return None
        except Exception as e:
            print(f"Error scraping profile: {e}")
            return None

def process_image(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            # Convert image to grayscale and then to numpy array
            img_array = np.array(img.convert('L'))
            return img_array
        else:
            return None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def save_to_database(name, organization, linkedin_url, facial_encoding):
    try:
        profile = Profile(name=name, organization=organization, linkedin_url=linkedin_url, facial_encoding=facial_encoding)
        db.session.add(profile)
        db.session.commit()
        print("Profile saved to database.")
    except Exception as e:
        print(f"Error saving profile to database: {e}")
        db.session.rollback()


urls = [
    "https://www.linkedin.com/in/ritikraj26/",
]

scrape_profile(urls)