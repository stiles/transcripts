import yt_dlp
import os
import re

# Ensure the "audio" directory exists
audio_dir = 'audio/raw/'
if not os.path.exists(audio_dir):
    os.makedirs(audio_dir)

# Replace this URL with the YouTube video you want to download
video_url = "https://www.youtube.com/watch?v=hBMoPUAeLnY"

# Function to slugify the video title
def slugify(title):
    # Convert to lowercase
    title = title.lower()
    # Replace spaces and other unwanted characters with hyphens
    title = re.sub(r'[\s\W-]+', '-', title)
    # Remove leading/trailing hyphens
    return title.strip('-')

# Options to download only audio
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': os.path.join(audio_dir, '%(title)s.%(ext)s'),
}

# Download the audio
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(video_url, download=False)  # Extract video info
    video_title = info_dict.get('title', 'audio')  # Get the title
    slugified_title = slugify(video_title)  # Slugify the title
    
    # Update the output template with the slugified title
    ydl_opts['outtmpl'] = os.path.join(audio_dir, f'{slugified_title}.%(ext)s')
    
    # Download with the updated options
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

print("Audio downloaded successfully!")
