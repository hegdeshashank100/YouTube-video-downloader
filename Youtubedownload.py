import streamlit as st
from pytube import YouTube
import moviepy.editor as mp
import os

# Page configuration
st.set_page_config(page_title="YouTube Video Downloader", page_icon=":tada:", layout="centered")

# Page content
st.subheader("Hello There, Welcome To This Page")
st.title("Here you can download YouTube videos for free")
st.write("by [Shashank Hegde](https://www.instagram.com/shashank.hegde.2805?igsh=eHU2dGtpaHIydjIz)")

# Text input for URL
url = st.text_input("Enter URL")

# Buttons for Low and High Quality options
col1, col2 = st.columns(2)
with col1:
    low_quality = st.button("Low Quality")
with col2:
    high_quality = st.button("High Quality")

def high_quality_download(url):
    try:
        # Create a YouTube object with the provided URL
        yt = YouTube(url)
    
        # Get the title of the video and sanitize it for filenames
        title = yt.title
        safe_title = "".join([c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in title])  # Sanitize title for use in filenames
    
        # Get the highest quality video and audio streams
        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).first()
    
        # Define filenames based on the video title
        video_filename = f'{safe_title}_video.mp4'
        audio_filename = f'{safe_title}_audio.mp4'
        final_filename = f'{safe_title}.mp4'
    
        # Download video and audio
        video_stream.download(filename=video_filename)
        audio_stream.download(filename=audio_filename)
    
        # Merge video and audio
        video_clip = mp.VideoFileClip(video_filename)
        audio_clip = mp.AudioFileClip(audio_filename)
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.write_videofile(final_filename, codec='libx264', audio_codec='aac')
    
        # Provide download button for the final video
        with open(final_filename, "rb") as uploaded_file:
            st.download_button(
                label="Download video",
                data=uploaded_file,
                file_name=final_filename,
                mime='video/mp4'
            )
    
        # Clean up temporary files
        os.remove(video_filename)
        os.remove(audio_filename)
        os.remove(final_filename)
    
        st.success(f"Downloaded and merged '{yt.title}' successfully as '{final_filename}'!")

    except Exception as e:
        st.error(f"An error occurred: {e}")

def low_quality_download(url):
    try:
        # Create a YouTube object
        yt = YouTube(url)
        ys = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
    
        # Define the filename based on the video title
        title = yt.title
        safe_title = "".join([c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in title])
        file_name = f'{safe_title}.mp4'
    
        # Download the video
        file_path = ys.download(filename=file_name)
    
        # Provide download button for the video
        with open(file_path, "rb") as uploaded_file:
            st.download_button(
                label="Download video",
                data=uploaded_file,
                file_name=file_name,
                mime='video/mp4'
            )
    
        st.success(f"Download completed! The file name is: {file_name}")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Check which button was clicked
if low_quality:
    if url:
        low_quality_download(url)
    else:
        st.error("Please enter a URL to download.")
    
if high_quality:
    if url:
        st.write("It will take time")
        high_quality_download(url)
    else:
        st.error("Please enter a URL to download.")