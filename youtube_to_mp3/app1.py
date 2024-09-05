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

st.title("YouTube to :blue[MP3 Downloader]")

st.markdown('<p style="color:green;">Enter the Google Sheets link with YouTube URLs</p>', unsafe_allow_html=True)
google_sheets_link = st.text_input("Enter the Google Sheets link:")

st.markdown('<p style="color:green;">Select the output directory:</p>', unsafe_allow_html=True)
output_dir_options = ['Downloads', 'Documents', 'Desktop']
output_dir_default = 'Downloads'
output_dir = st.selectbox("Select the output directory:", output_dir_options, index=output_dir_options.index(output_dir_default))

if os.name == 'nt':  # Windows
    root_dir = f"C:\\Users\\{os.getlogin()}\\"
else:  # macOS/Linux
    root_dir = f"~/"

output_dir_path = os.path.join(root_dir, output_dir, 'YouTube_MP3_Downloader')

if google_sheets_link:
    # Download the Google Sheets file as an Excel file
    file_id = google_sheets_link.split('/')[-2]
    output = 'temp.xlsx'
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

    # Load the Excel file
    df = pd.read_excel(output)

    st.write("Google Sheets file loaded successfully!")
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
                    download_video_as_mp3(url, output_dir_path)
                    st.success(f"Downloaded {url}")
                except Exception as e:
                    st.error(f"Failed to download {url}: {e}")

            st.write("Downloads completed!")
    else:
        st.error("The Google Sheets file must contain a 'Links' column with YouTube URLs.")

    # Remove the temporary Excel file
    os.remove(output)

if st.button(":red[Output Directory]"):
    if os.path.exists(output_dir_path):
        st.write(f"MP3 files are saved in the '{output_dir_path}' directory.")
    else:
        st.error("No MP3 files downloaded.")