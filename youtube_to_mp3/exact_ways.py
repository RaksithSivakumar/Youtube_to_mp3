import streamlit as st
import pandas as pd
import yt_dlp
import os
import gdown

def download_video_as_mp3(youtube_url, output_path):
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

st.set_page_config(page_title="YouTube to MP3 Downloader", page_icon=":purple[MP3]", layout="wide", initial_sidebar_state="expanded")

st.markdown('<style>body { background-color: #f0f0f0; }</style>', unsafe_allow_html=True)
st.markdown('<style>#MainMenu {visibility: hidden;}</style>', unsafe_allow_html=True)

st.title(":blue[Ways] YouTube to MP3 Downloader")
st.markdown('<p style="color:#9C27B0;">A simple tool to download YouTube videos as MP3 files.</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<p style="color:#E91E63;">Enter the Google Sheets link with YouTube URLs:</p>', unsafe_allow_html=True)
    google_sheets_link = st.text_input("Google Sheets link:", placeholder="https://drive.google.com/...")

with col2:
    st.markdown('<p style="color:#2196F3;">Select the output directory:</p>', unsafe_allow_html=True)
    output_dir_options = ['Downloads', 'Documents', 'Desktop']
    output_dir_default = 'Downloads'
    output_dir = st.selectbox("Output directory:", output_dir_options, index=output_dir_options.index(output_dir_default))

if os.name == 'nt':  
    root_dir = f"C:\\Users\\{os.getlogin()}\\"

output_dir_path = os.path.join(root_dir, output_dir, 'YouTube_MP3_Downloader')

if google_sheets_link:
    file_id = google_sheets_link.split('/')[-2]
    output = 'temp.xlsx'
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

    df = pd.read_excel(output)

    st.write("Google Sheets file loaded successfully!")
    st.write("Preview of the file:")
    st.dataframe(df.head())

    if 'Links' in df.columns:
        urls = df['Links'].tolist()

        if st.button(":yellow[Download MP3s]"):
            st.write("Starting download....")

            for i, url in enumerate(urls):
                try:
                    st.write(f"Downloading {i+1}/{len(urls)}: {url}")
                    download_video_as_mp3(url, output_dir_path)
                    st.success(f"Downloaded {url}")
                except Exception as e:
                    st.error(f"Failed to download {url}: {e}")

            st.write("Downloads completed!")
    else:
        st.error("The Google Sheets file must contain a 'Links' column with YouTube URLs.")

    os.remove(output)

if st.button("Exact"):
    if os.path.exists(output_dir_path):
        st.write(f"MP3 files are saved in the '{output_dir_path}' directory.")
    else:
        st.error("No MP3 files downloaded.")