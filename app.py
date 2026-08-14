from flask import Flask,request,render_template,send_from_directory
import os
from werkzeug.utils import secure_filename
app=Flask(__name__)
print("APP: ",app)
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
print("Base directory: ",BASE_DIR)
UPLOAD_FOLDER=os.path.join(BASE_DIR,"assets","uploads")
print("UPLOAD FOLDER: ",UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
@app.route("/",methods=["POST","GET"])
def index():
    return render_template("index.html")
@app.route("/upload",methods=["GET","POST"])
def upload():
    #return to home page if there is no file yet
    if request.method=="GET":
        return render_template("upload.html")
    file=request.files.get("file")
    print("File: ",file)
    if not file:
        return "No file uploaded",400
    if file.filename=="":
        return "No file selected",400
    filename=secure_filename(file.filename)
    print("File name: ",filename)
    if not filename.lower().endswith(".docx"):
        return "Only .docx files are allowed",400
    file_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
    print("Saving to: ",file_path)
    file.save(file_path)
    return "File uploaded successfully"


#download files
@app.route("/download/<filename>",methods=['POST','GET'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
    filename,
    as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)