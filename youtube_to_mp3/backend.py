import yt_dlp
import pandas as pd
import os

# Define the function to download a single video as MP3
def download_video_as_mp3(youtube_url, output_path='output'):
    # Ensure the output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Define options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    # Download and convert the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

# Load the Excel file containing YouTube URLs
file_path = '/content/time signature 4_4 dataset.xlsx'  # Replace with your Excel file path
df = pd.read_excel(file_path)

# Assume the column containing the URLs is named 'URL'
urls = df['Links'].tolist()

# Loop through the list of URLs and download each as MP3
for url in urls:
    download_video_as_mp3(url)