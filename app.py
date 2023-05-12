from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
from os import listdir
from os.path import isfile, join

cpath = os.getcwd()
cpath.replace("\\", "/")

app = Flask(__name__)
mypath = (cpath + "/static/links")

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/result.html')
def result():
    return render_template('result.html')

@app.route('/helppage.html')
def helppage():
    return render_template('helppage.html')

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    image = request.files['image']
    image.save('input.png')
    proc = subprocess.Popen("backend.py", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    (output, err) = proc.communicate()
    proc_status = proc.wait()
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    linklist = []
    nlist = []
    x = 0
    for file in onlyfiles:
        f = open(file, "r")
        ll = [i.strip() for i in f.readlines()]
        linklist.append([{'src': f'static/downloaded_images/{x}/image{i}{j}.jpg', 'link': ll[i*j]} for i in range(5) for j in range(3)])
        nlist.append(ll[-1])
        x += 1
    return render_template('result.html', grid_data = linklist, grid_len = len(linklist), name_data = nlist)

if __name__ == "__main__":
    app.run(debug=True)