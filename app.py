# accent_detector/app.py
import streamlit as st
import os
import tempfile
import requests
from utils.transcriber import transcribe_audio
from utils.classifier import classify_accent
from utils.downloader import download_video, extract_audio
import time

st.set_page_config(
    page_title="Accent Analyzer",
    page_icon="🌍",
    layout="wide",
    menu_items={
        'About': "Accent Analysis Tool | REM Waste Hiring Assessment"
    }
)

st.title("🌍 English Accent Analyzer")
st.markdown("""
**Evaluate spoken English proficiency for hiring purposes**  
*Analyze accent characteristics and speaking clarity from any video*
""")

# Input section
url = st.text_input("Enter video URL (YouTube, Loom, or direct link):", 
                   placeholder="https://example.com/video.mp4")

if st.button("Analyze Accent", type="primary", use_container_width=True):
    if not url:
        st.warning("Please enter a video URL")
        st.stop()
    
    # Setup processing
    progress_bar = st.progress(0)
    status = st.empty()
    results_placeholder = st.empty()
    
    try:
        start_time = time.time()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Step 1: Download video
            status.subheader("🔽 Step 1: Downloading video...")
            video_path = download_video(url, temp_dir)
            progress_bar.progress(25)
            st.toast(f"Downloaded video in {time.time()-start_time:.1f}s", icon="✅")
            
            # Step 2: Extract audio
            status.subheader("🎵 Step 2: Extracting audio...")
            audio_path = extract_audio(video_path, temp_dir)
            progress_bar.progress(50)
            st.toast(f"Audio extracted in {time.time()-start_time:.1f}s", icon="✅")
            
            # Step 3: Transcribe
            status.subheader("📝 Step 3: Transcribing speech...")
            transcription = transcribe_audio(audio_path)
            progress_bar.progress(75)
            st.toast(f"Transcribed speech in {time.time()-start_time:.1f}s", icon="✅")
            
            # Step 4: Classify accent
            status.subheader("🔍 Step 4: Analyzing accent...")
            accent_result = classify_accent(audio_path)
            progress_bar.progress(100)
            st.toast(f"Accent analyzed in {time.time()-start_time:.1f}s", icon="✅")
            
            # Display results
            st.success("✅ Analysis Complete!")
            st.audio(audio_path, format="audio/wav")
            
            # Results layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Accent Classification")
                st.markdown(f"### {accent_result['accent']}")
                st.metric("Confidence Score", f"{accent_result['confidence']:.1f}%")
                
            with col2:
                st.subheader("Accent Distribution")
                for label, score in accent_result['all_scores'].items():
                    st.progress(score, text=f"{label}: {score*100:.1f}%")
            
            # Transcription
            with st.expander("View Transcript"):
                st.write(transcription)
            
            # Interpretation
            with st.expander("Analysis Summary"):
                st.markdown(f"""
                **Speaker's Accent:** {accent_result['accent']}  
                **Confidence:** {accent_result['confidence']:.1f}%  
                **English Transcription:**  
                {transcription}
                
                **Interpretation:**  
                The speaker demonstrates {'strong' if accent_result['confidence'] > 85 else 'clear' if accent_result['confidence'] > 70 else 'moderate'} 
                characteristics of a {accent_result['accent']} accent.
                """)
    
    except Exception as e:
        error_msg = str(e)
        
        # Special handling for common errors
        if "Video unavailable" in error_msg:
            st.error("❌ YouTube video unavailable. This may be due to age restrictions, region blocks, or copyright claims.")
        elif "403" in error_msg or "Forbidden" in error_msg:
            st.error("❌ Server blocked the download. Please try a different URL.")
        elif "too long" in error_msg:
            st.error("❌ Video too long. Maximum duration is 5 minutes.")
        else:
            st.error(f"❌ Processing error: {error_msg}")
        
        # Troubleshooting tips
        with st.expander("Troubleshooting Tips", expanded=True):
            st.markdown("""
            **Try these solutions:**
            1. Use a different video URL
            2. Try shorter videos (under 2 minutes)
            3. Ensure clear English speech
            4. Use one of these sample URLs:
               - `https://download.samplelib.com/mp4/sample-5s.mp4`
               - `https://www.youtube.com/watch?v=8UQzCQ4I7X0`
            """)

# Footer
st.markdown("---")
st.caption("Accent Analysis System v1.0 | Uses Whisper and SpeechBrain AI models")