import os, requests, lxml, re, json, urllib.request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5060.114 Safari/537.36"
}

search_params = {
    "q": "ferrari logos png", # the search term
    "tbm": "isch",
    "hl": "en",
    "gl": "us",
    "ijn": "0"
}

# making the request to Google's search API
response = requests.get("https://www.google.com/search", params=search_params, headers=request_headers, timeout=30)
# creating a BeautifulSoup object from the HTML
page_content = BeautifulSoup(response.text, "lxml")

def extract_images_with_request_headers():
    del search_params["ijn"]
    search_params["content-type"] = "image/png" # parameter to specify the original media type
    return [image["src"] for image in page_content.select("img")]

def generate_suggested_search_data():
    search_suggestions = []
    scripts = page_content.select("script")
    extracted_images = "".join(re.findall(r"AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>", str(scripts)))
    fixed_extracted_images_data = json.dumps(extracted_images)
    json_extracted_images_data = json.loads(fixed_extracted_images_data)
    suggested_search_thumbnail_data = ",".join(re.findall(r'{key(.*?)\[null,\"Size\"', json_extracted_images_data))
    encoded_suggested_search_thumbnail = re.findall(r'\"(https:\/\/encrypted.*?)\"', suggested_search_thumbnail_data)
    for suggested_search, thumbnail in zip(page_content.select(".PKhmud.sc-it.tzVsfd"), encoded_suggested_search_thumbnail):
        search_suggestions.append({
            "name": suggested_search.select_one(".VlHyHc").text,
            "link": f"https://www.google.com{suggested_search.a['href']}",
            "chips": "".join(re.findall(r"&chips=(.*?)&", suggested_search.a["href"])),
            "thumbnail": bytes(thumbnail, "ascii").decode("unicode-escape")
        })
    return search_suggestions

def retrieve_original_images():
    google_img_data = []
    scripts = page_content.select("script")
    extracted_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(scripts)))
    fixed_extracted_images_data = json.dumps(extracted_images_data)
    json_extracted_images_data = json.loads(fixed_extracted_images_data)
    google_image_data = re.findall(r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}', json_extracted_images_data)
    google_images_thumbnail_data = ", ".join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(google_image_data))).split(", ")
    thumbnail_images = [
        bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in google_images_thumbnail_data
    ]
    removed_google_images_thumbnail_data = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(google_image_data))
    google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_google_images_thumbnail_data)
    full_resolution_images = [
        bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in google_full_resolution_images
    ]
    for count, (metadata, thumbnail, original) in enumerate(zip(page_content.select('.isv-r.PNCib.MSM1fd.BUooTd'), thumbnail_images, full_resolution_images), start=1):
        google_img_data.append({
            "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"],
            "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["href"],
            "source": metadata.select_one(".fxgdke").text,
            "thumbnail": thumbnail,
            "original": original
        })
        print(f'Downloading image {count}...')
        url_opener = urllib.request.build_opener()
        url_opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')]
        urllib.request.install_opener(url_opener)
        urllib.request.urlretrieve(original, f'/work/Images/TestLogos/{search_params["q"][:search_params["q"].find(" ")]}_{count}.jpg')
    return google_img_data