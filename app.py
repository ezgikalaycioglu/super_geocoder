from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import csv
import pandas as pd
from html_table import csvtohtml
from findcoords import coords,show_in_map


app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        file=request.files["file"]
        new_filename="uploaded_"+file.filename
        file.save(secure_filename(new_filename))
        try:
            data=pd.read_csv(new_filename ,encoding = 'utf-8')
            if "Address" in data.columns or "address" in data.columns:
                file_with_coord=coords(new_filename)
                csvtohtml("file_withcoords.csv")
                show_in_map("file_withcoords.csv")
                return render_template('success.html', btn1="mapbutton.html", btn2="download.html")
            else:
                return render_template('index.html',text="Please make sure that you have an adress column in your csv file")
        except:
            return render_template('index.html',text="Please make sure that you have uploaded a csv file")

@app.route("/Map_html_coords")
def Map_html_coords():
    return render_template("Map_html_coords.html")

@app.route("/download.html")
def download_file():
    return send_file("file_withcoords.csv", attachment_filename="coordinates.csv", as_attachment=True)

if __name__=='__main__':
    app.debug=True
    app.run()