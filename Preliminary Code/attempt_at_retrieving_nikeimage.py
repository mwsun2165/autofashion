import requests
from bs4 import BeautifulSoup
import os
import base64
from io import BytesIO
from PIL import Image
from googlesearch import search

search_string = "red shoe"

base_url = "https://www.nike.com"

search_url = base_url + "/w?q=" + search_string

response = requests.get(search_url)
soup = BeautifulSoup(response.content, "html.parser")

product_images = soup.find_all("img", {"class": "product-card__hero-image"})

if not os.path.exists(search_string):
    os.makedirs(search_string)

for i, image in enumerate(product_images):
    # print(i)
    image_url = image.get("src")
    if image_url is not None:
        if image_url.startswith("//"):
            image_url = "https:" + image_url
        elif not image_url.startswith("http"):
            image_url = base_url + "/" + image_url
        if image_url.startswith("data:image"): #for 64bit image
            image_data = base64.b64decode(image_url.split(",")[1])
            img = Image.open(BytesIO(image_data))
            image_filename = os.path.join(search_string, f"{search_string}_{i}.jpg")
            img.save(image_filename)
        else:
            image_filename = os.path.join(search_string, f"{search_string}_{i}.jpg")
            response = requests.get(image_url)
            with open("/work/" + image_filename, "wb") as f: #"/work/"
                f.write(response.content)

query = "nike red shoe" #same as string we're looking for, but with brand appended at the front
for j in search(query, tld="co.in", num=10, stop=10, pause=2):
    print(j)

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")
 
# to search
query = "nike red shoe"
for j in search(query, tld="co.in", num=10, stop=10, pause=2):
    print(j)