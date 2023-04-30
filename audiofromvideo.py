
# Python code to convert video to audio
import moviepy.editor as mp
import os

UPLOAD_FOLDER_VIDEO = "UserVideo"
UPLOAD_FOLDER_AUDIO = "UserAudio"

def saveaudiofromvideo(path):  
    # Insert Local Video File Path 
    clip = mp.VideoFileClip(os.path.join(UPLOAD_FOLDER_VIDEO, path))
    
    # Insert Local Audio File Path
    clip.audio.write_audiofile(os.path.join(UPLOAD_FOLDER_AUDIO, path[:-3]+"mp3"))

    # if os.path.exists(os.path.join(UPLOAD_FOLDER_VIDEO, path)):
    #     os.remove(os.path.join(UPLOAD_FOLDER_VIDEO, path))

    return


if __name__ == "__main__":

    path = "joeyhate.mp4"
    saveaudiofromvideo(path)