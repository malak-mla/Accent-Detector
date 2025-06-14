# accent_detector/utils/downloader.py
import os
import requests
import yt_dlp
import validators
from moviepy.editor import VideoFileClip
import re
import random  # Added missing import

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

def download_video(url: str, temp_dir: str) -> str:
    """Download video from any public URL"""
    if not validators.url(url):
        raise ValueError("Invalid URL format")
    
    # Extract YouTube video ID
    youtube_id = extract_youtube_id(url)
    
    if youtube_id:
        return download_youtube_video(youtube_id, temp_dir)
    
    # Direct video download
    return download_direct_video(url, temp_dir)

def extract_youtube_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    patterns = [
        r"youtube\.com/watch\?v=([^&]+)",
        r"youtu\.be/([^?]+)",
        r"youtube\.com/embed/([^/]+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def download_youtube_video(video_id: str, temp_dir: str) -> str:
    """Download YouTube video using yt-dlp"""
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, 'video.%(ext)s'),
        'quiet': True,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'noplaylist': True,
        'ignoreerrors': True,
        'retries': 3,
        'user-agent': random.choice(USER_AGENTS),  # Now works with random imported
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if not info:
            raise RuntimeError("Failed to download YouTube video")
        return ydl.prepare_filename(info)

def download_direct_video(url: str, temp_dir: str) -> str:
    """Download direct video file"""
    headers = {
        'User-Agent': random.choice(USER_AGENTS),  # Now works with random imported
        'Referer': 'https://www.google.com/',
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        # Get filename from URL
        filename = url.split('/')[-1].split('?')[0]
        if '.' not in filename:
            filename = "video.mp4"
        
        video_path = os.path.join(temp_dir, filename)
        
        with open(video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        
        return video_path
    except Exception as e:
        raise RuntimeError(f"Direct download failed: {str(e)}")

def extract_audio(video_path: str, temp_dir: str) -> str:
    """Extract audio from video file"""
    audio_path = os.path.join(temp_dir, "audio.wav")
    
    try:
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
        return audio_path
    except Exception as e:
        raise RuntimeError(f"Audio extraction failed: {str(e)}")