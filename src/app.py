from flask import Flask,render_template, request,flash,redirect
import os
from werkzeug.utils import secure_filename
import compressAlgo

app = Flask(__name__)

app.secret_key = "himitsu desu"
app.config["Image_upload"] = os.getcwd() + "\\static\\img\\base\\"
app.config["Image_compressed"] = os.getcwd() + "\\static\\img\\compressed\\"
app.config["ALLOWED_EXTENSIONS"] = ['png', 'jpg', 'jpeg', 'gif']

filename = ""
def isallowed(filename):
    if not "." in filename:
        return False    
    ext = filename.rsplit('.',1)[1] 

    if ext.lower() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('index.html',filename = filename, compress = False)

@app.route('/', methods=['GET','POST'])
def upload_image():
    global filename
    if request.method == 'POST':
        if request.files:
            image = request.files["image"]

            if image.filename == "":
                return redirect(request.url)
            if not isallowed(image.filename):
                return redirect(request.url)
            
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["Image_upload"],filename))

            return render_template('index.html',filename=filename,compress = False)
        elif request.form.get("compress_button"):
            compressAlgo.algo(filename)
            return render_template('index.html', filename = filename, compress = True)
    return render_template('index.html',filename = filename, compress = False)



if __name__ == "__main__":
    app.run(debug=True)