import streamlit as st
import pandas as pd
import yt_dlp
import os

def download_video_as_mp3(youtube_url, output_path='output'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

st.title("YouTube to :blue[MP3 Downloader]")

st.markdown('<p style="color:green;">Upload your Excel file with YouTube URLs</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=['xlsx'])

if uploaded_file:
        # Display the Excel file
    df = pd.read_excel(uploaded_file)
    st.write("Excel file uploaded successfully!")
    st.write("Preview of the file:")
    st.dataframe(df.head()) 

    # 'Links' column exists
    if 'Links' in df.columns:
        urls = df['Links'].tolist()
        
        # trigger MP3 download
        if st.button("Download MP3s"):
            st.write("Starting download....")

            for i, url in enumerate(urls):
                try:
                    st.write(f"Downloading {i+1}/{len(urls)}: {url}")
                    download_video_as_mp3(url)
                    st.success(f"Downloaded {url}")
                except Exception as e:
                    st.error(f"Failed to download {url}: {e}")

            st.write("Downloads completed!")
    else:
        st.error("The Excel file must contain a 'Links' column with YouTube URLs.")

if st.button(":red[Output Directory]"):
    output_dir = 'output'
    if os.path.exists(output_dir):
        st.write(f"MP3 files are saved in the '{output_dir}' directory.")
    else:
        st.error("No MP3 files downloaded.")
