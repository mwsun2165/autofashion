import subprocess
import os
import shutil
import time
import openai
import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.request
from dotenv import load_dotenv
load_dotenv()

cdlist = ["undef", "Anorak", "Blazer", "Blouse", "Bomber", "Button-Down", "Cardiagn", "Flannel", "Halter", "Henley", "Hoodie", "Jacket", "Jersey", "Parka", "Peacoat", "Poncho", "Sweater", "Tank", "Tee", "Top", "Turtleneck", "Capris", "Chinos", "Culottes", "Cutoffs", "Gauchos", "Jeans", "Jeggings", "Jodhpurs", "Joggers", "Leggings", "Sarong", "Shorts", "Skirt", "Sweatpants", "Sweatshorts", "Trunks", "Caftan", "Cape", "Coat", "Coverup", "Dress", "Jumpsuit", "Kaftan", "Kimono", "Nightdress", "Onesie", "Robe", "Romper", "Shirtdress", "Sundress"]
ldlist = ["Under Armour", "Reebok", "Nike", "undef", "Columbia", "Adidas"]

cpath = os.getcwd()
cpath.replace("\\", "/")

yolo_path = cpath + "yolov5"
static_path = cpath + "static"
img_path = static_path + "/downloaded_images"
lnk_path = static_path + "/links"

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

with cd(cpath + "yolov5"):
    proc = subprocess.Popen("python detect.py --source " + cpath + "input.png" + " --weights clothing.pt --conf 0.25 --save-txt" ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    outpt = proc.communicate()[0].split()
    for i in outpt:
        if b"runs\\detect\\exp" in i:
            newfl = "/" + str(i)[9:-7] + "/input.png"
            newfl = newfl.replace("\\", "/")
            break
    subprocess.Popen("python detect.py --source " + yolo_path + newfl + " --weights labels.pt --conf 0.25 --save-txt" ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

ct, ot, loc = "", "", 0
for x in range(len(newfl)):
    if newfl[x].isnumeric(): ct, loc = ct+newfl[x], x
    else: ot += newfl[x]
for i in range(len(newfl)):
    if newfl[i].isnumeric():
        loc = i
        break
ct = (int(ct)+1, 1)[len(ct) == 0]
fnfl = yolo_path + "/" + ot[0:loc] + str(ct) + ot[loc:]
while(not os.path.exists(fnfl)): time.sleep(1)

for filename in os.listdir(static_path):
    file_path = os.path.join(static_path, filename)
    if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)

shutil.move(fnfl, static_path)
ta, tb = fnfl, yolo_path + newfl
rem1 = ta[::-1].find('/')
sf1, sf2 = ta[:-1*rem1] + "labels/input.txt", tb[:-1*rem1] + "labels/input.txt"
if os.path.isfile(sf1):
    with open(sf1) as file:
        llist = [line.rstrip().split(" ") for line in file]
else:
    llist = []
if os.path.isfile(sf2):
    with open(sf2) as file:
        clist = [line.rstrip().split(" ") for line in file]
else:
    clist = []
clist, llist = [[float(i) for i in x] for x in clist], [[float(i) for i in x] for x in llist]

clothes = []
for i in clist:
    if len(llist) == 0:
        clothes.append([cdlist[int(i[0])]])
    else:
        for j in llist:
            if j[1]-j[3]/2 > i[1]-i[3]/2 and j[1]+j[3]/2 < i[1]+i[3]/2 and j[2]-j[4]/2 > i[2]-i[4]/2 and j[2]+j[4]/2 < i[2]+i[4]/2:
                clothes.append([ldlist[int(j[0])], cdlist[int(i[0])]])
                break


openai.api_key = os.getenv('openai_key')
model_engine = "text-davinci-002"

def generate_text(prompt):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=1.5,
        top_p=0.5,
    )
    message = completions.choices[0].text
    return message.strip()

results = []
for k in range(len(clothes)):
    if len(clothes[k]) == 2:
        brand, cloth_type = clothes[k][0], clothes[k][1]
        prompt = f"""List 5 different brands (PLEASE INCLUDE THE {brand} ITSELF) that make {cloth_type} similar to {brand}, and recommend 3 specific {cloth_type} models from each brand with their unique product names or model numbers in the following format:
        1. Brand1-item1; item2; item3
        2. Brand2-item1; item2; item3
        3. Brand3-item1; item2; item3
        4. Brand4-item1; item2; item3
        5. Brand5-item1; item2; item3
        DOUBLE CHECK THAT EACH RECOMMENDATION IS ACTUALLY {cloth_type}, DO NOT RECOMMEND ITEMS THAT DO NOT EXIST OR IS NOT {cloth_type}
        """
    else:
        cloth_type = clothes[k][0]
        prompt = f"""List 5 different brands that make good high quality {cloth_type}, and recommend 3 specific {cloth_type} models from each brand with their unique product names or model numbers in the following format:
        1. Brand1-item1; item2; item3
        2. Brand2-item1; item2; item3
        3. Brand3-item1; item2; item3
        4. Brand4-item1; item2; item3
        5. Brand5-item1; item2; item3
        DOUBLE CHECK THAT EACH RECOMMENDATION IS ACTUALLY {cloth_type}, DO NOT RECOMMEND ITEMS THAT DO NOT EXIST OR IS NOT {cloth_type}
        """
    
    pre_split = generate_text(prompt)
    response = pre_split.split("\n")
    temp = []
    for r in response:
        dash = r.find("-")
        temp_brand = r[3:dash]
        i1 = r.find(";", dash + 1)
        item1 = r[dash + 1:i1]
        i2 = r.find(";", i1 + 2)
        item2 = r[i1 + 2:i2]
        item3 = r[i2 + 2:]
        if item3[-1] == ' ': item3 = item3[:-1]
        temp.append((temp_brand, [item1, item2, item3]))
    results.append(temp)


def get_original_images(keyword, i, name):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"}
    params = {
        "q": keyword, # search query
        "tbm": "isch", # image results
        "hl": "en",    # language of the search
        "gl": "us",    # country where search comes from
    }

    html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, "lxml")

    all_script_tags = soup.select("script")
    matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)
    matched_google_image_data = re.findall(r'\"GRID_STATE0\"(.*)sideChannel:\s?{}}', matched_images_data_json)
    matched_google_images_thumbnails = ", ".join(re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', str(matched_google_image_data))).split(", ")
    thumbnails = [bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails]
    removed_matched_google_images_thumbnails = re.sub(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))
    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)
    full_res_images = [bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images]

    first_image_url = full_res_images[0] if full_res_images else None

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(first_image_url, img_path + f'/{str(i)}/{name}.jpg')
        
if not os.path.exists(img_path):
    os.makedirs(img_path)

for filename in os.listdir(img_path):
    file_path = os.path.join(img_path, filename)
    if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
links_images = []
for i, r in enumerate(results):
    temp_links = []
    if not os.path.exists(os.path.join(img_path, str(i))):
        os.makedirs(os.path.join(img_path, str(i)))
    for a, brands in enumerate(r):
        for k in range(len(brands[1])):
            temp = brands[0] + " " + brands[1][k]
            get_original_images(temp, i, "image" + str(a) + str(k))
            temp_links.append("https://www.google.com/search?q=" + "%20".join(temp.split())) # converting to google search links
    links_images.append(temp_links)

if not os.path.exists(lnk_path):
    os.makedirs(lnk_path)

for i in range(0, int(len(links_images)/15)):
    while True:
        if os.path.exists(lnk_path + f"/links_{i}.txt"): os.remove(lnk_path + f"/links_{i}.txt")
        else: break
    for k in range(len(links_images)):
        with open(lnk_path + f"/links_{k}.txt", "w") as f:
            for l in links_images[k]:
                f.write(l + "\n")
        f.close()
