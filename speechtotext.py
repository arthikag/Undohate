# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub

    if path.endswith('.mp3') or path.endswith('.MP3'):
            sound = AudioSegment.from_mp3(path)
    elif path.endswith('.wav') or path.endswith('.WAV'):
        sound = AudioSegment.from_wav(path)
    elif path.endswith('.ogg'):
        sound = AudioSegment.from_ogg(path)
    elif path.endswith('.flac'):
        sound = AudioSegment.from_file(path, "flac")
    elif path.endswith('.3gp'):
        sound = AudioSegment.from_file(path, "3gp")
    elif path.endswith('.3g'):
        sound = AudioSegment.from_file(path, "3gp")

    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                # print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text

if __name__ == "__main__":
    path = "UserAudio/test2.mp3"
    print("\nFull text:", get_large_audio_transcription(path))
