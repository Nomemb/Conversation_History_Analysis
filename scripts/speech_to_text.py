import speech_recognition as sr
import os
from pydub import AudioSegment

folder_path = "C:/Users/Admin/Desktop/Conversation_History_Analysis/dataset/raw_data/audio_file"
output_path = "C:/Users/Admin/Desktop/Conversation_History_Analysis/dataset/raw_data/result_file"
audio_list = []


for file in os.listdir(folder_path):
    file_path = f"{folder_path}/{file}"
    save_path = f"{output_path}/{file}"
    print(file_path)
    try:
        audio = AudioSegment.from_mp3(file_path)
        audio.export(save_path, format='wav')

    except Exception as e:
        print(f"Error converting {file}: {e}")