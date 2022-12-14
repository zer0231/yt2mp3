from flask import Flask, redirect, url_for, render_template, request, session,flash,send_file
from yt_handler import download_to_mp3, convert_to_zip
import concurrent.futures

app = Flask(__name__)
app.secret_key = 'TheMostComplicatedSecretKey'


def download_and_convert(yt_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_to_mp3,yt_list)
    return convert_to_zip()

# def verify_urls(url):
    #return true if url is valid else false

@app.route('/',methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template('index.html',title="YouTube-To-Mp3")
    if request.method == "POST":
        url_list = []
        urls = request.form.to_dict().values()
        for url in urls:
            url_list.append(url)
        print(url_list)
        outputfile_name = download_and_convert(url_list)
        print(outputfile_name)
        return send_file('./tmp/archives/'+outputfile_name+'.zip', as_attachment=True)
        return render_template('index.html',title="Convert finish")

if __name__ == "__main__":
    app.run(debug=True)
    