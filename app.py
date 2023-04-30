from flask import Flask
from flask import render_template, redirect, request, send_from_directory

from werkzeug.utils import secure_filename
import os

from hatedetector import hatedetectorfunc
from badwords import bad_words_highlight
from sentiment import sentimentfunc
from speechtotext import get_large_audio_transcription
from imagetotext import get_image_transcription
from audiofromvideo import saveaudiofromvideo
from emoDetectv1 import emotion
from tweetsanalysis import tweetAnalysis

UPLOAD_FOLDER_AUDIO = "UserAudio"
ALLOWED_EXTENSIONS_AUDIO = {'mp3', 'wav', 'ogg', 'flac', '3gp', '3g'}

UPLOAD_FOLDER_IMAGE = "UserImage"
ALLOWED_EXTENSIONS_IMAGE = {'jpg', 'jpeg', 'png', 'tiff'}

UPLOAD_FOLDER_VIDEO = "UserVideo"
ALLOWED_EXTENSIONS_VIDEO = {'mp4', 'mov', 'mkv', 'wmv'}

def allowed_file_audio(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_AUDIO

def allowed_file_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE

def allowed_file_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_VIDEO

def textAnalysisResult(text,type,emotionResult={},file=""):
    result = bad_words_highlight(text)
    isHate = "Hate" if result['isBad'] else "No Hate"
    if isHate == "Hate":
        text = result['rtext']
    else:
        isHate = "Hate" if hatedetectorfunc(text) else "No Hate"
    senti = sentimentfunc(text)
    if type == "image":
        print("succ")
        return render_template("result.html",file=file,hastext=True,text=text,isHate = isHate,sentiment=senti,type=type,emotionResult=emotionResult)
    else:
        return render_template("result.html",file=file,hastext=True,text=text,isHate = isHate,sentiment=senti,type=type)

app = Flask(__name__,static_url_path = "/static")

@app.route("/audiofile/<path:path>")
def static_dir1(path):
    return send_from_directory("UserAudio", path)

@app.route("/imagefile/<path:path>")
def static_dir2(path):
    return send_from_directory("UserImage", path)

@app.route("/videofile/<path:path>")
def static_dir3(path):
    return send_from_directory("UserVideo", path)

@app.route("/")
def home_page():
    return render_template("index.html") 

@app.route("/home")
def home_re():
    return redirect("/")

@app.route("/text",methods=['GET'])
def text_page():
    return render_template("text.html")

@app.route("/text",methods=['POST'])
def text_hate():
    return textAnalysisResult(request.form['message'],"text")

@app.route("/tweet",methods=['GET'])
def tweet_page():
    return render_template("tweetanalysis.html")

@app.route("/tweet",methods=['POST'])
def tweet_hate():
    results = tweetAnalysis(request.form['word'],int(request.form['count']))
    return render_template("tweetanalysisResult.html",keyword = request.form['word'], emotion = request.form['emotion'],result=results)

@app.route("/image",methods=['GET'])
def image_page():
    return render_template("image.html")

@app.route("/image",methods=['POST'])
def image_hate():
        # check if the post request has the file part
        if 'myfile' not in request.files:
            return redirect(request.url)
        file = request.files['myfile']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file_image(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER_IMAGE, filename))
            
            text = get_image_transcription(filename).strip()

            emotionResult = emotion(filename)

            if text == "":
                return render_template("result.html",file=filename,hastext=False,emotionResult=emotionResult,type="image")

            return textAnalysisResult(text,"image",file=filename,emotionResult=emotionResult)

        return redirect(request.url)

@app.route("/audio",methods=['GET'])
def audio_page():
    return render_template("audio.html")

@app.route("/audio",methods=['POST'])
def audio_hate():
        # check if the post request has the file part
        if 'myfile' not in request.files:
            return redirect(request.url)
        file = request.files['myfile']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file_audio(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER_AUDIO, filename))
            
            text = get_large_audio_transcription("UserAudio/"+filename)

            return textAnalysisResult(text,"audio",file=filename)
        return redirect(request.url)

@app.route("/video",methods=['GET'])
def video_page():
    return render_template("video.html")

@app.route("/video",methods=['POST'])
def video_hate():
        # check if the post request has the file part
        if 'myfile' not in request.files:
            return redirect(request.url)
        file = request.files['myfile']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file_video(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER_VIDEO, filename))

            saveaudiofromvideo(filename)

            text = get_large_audio_transcription("UserAudio/"+filename[:-3]+"mp3")

            if os.path.exists(os.path.join(UPLOAD_FOLDER_AUDIO, filename[:-3]+"mp3")):
                os.remove(os.path.join(UPLOAD_FOLDER_AUDIO, filename[:-3]+"mp3"))

            return textAnalysisResult(text,"video",file=filename)
        return redirect(request.url)

if __name__ == "__main__":
        app.run(debug=True)