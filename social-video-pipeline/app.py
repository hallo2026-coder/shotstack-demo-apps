import sys
from pathlib import Path

# Add the parent directory to Python's module search path
# This makes the 'shared' module importable when running on Render
sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from shared.shotstack_client import ShotstackClient
from shared.utils import chunk_text_for_scenes

load_dotenv()
app = Flask(__name__)
shotstack = ShotstackClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/render', methods=['POST'])
def render():
    data = request.json
    blog_text = data.get('blog_text', '')
    
    # Split into multiple scenes (each ≤ 280 chars)
    scenes = chunk_text_for_scenes(blog_text, max_chars_per_scene=280)
    if not scenes:
        return jsonify({'error': 'No text provided'}), 400
    
    # Build a multi-clip timeline with background music and lower thirds
    clips = []
    duration_per_clip = 5  # seconds
    start_time = 0
    
    for i, scene_text in enumerate(scenes):
        clips.append({
            "asset": {
                "type": "title",
                "text": scene_text,
                "style": "caption",
                "position": "center",
                "background": "#000000",
                "color": "#FFFFFF"
            },
            "start": start_time,
            "length": duration_per_clip,
            "effect": "fadeIn" if i == 0 else "fade"
        })
        start_time += duration_per_clip
    
    # Optional: add background music (using free asset)
    music_clip = {
        "asset": {
            "type": "audio",
            "src": "https://shotstack-assets.s3.amazonaws.com/music/upbeat.mp3"
        },
        "start": 0,
        "length": start_time,
        "effect": "fadeOutLast5"
    }
    
    timeline = {
        "timeline": {
            "background": "#000000",
            "tracks": [
                {"clips": clips},
                {"clips": [music_clip]}
            ]
        },
        "output": {
            "format": "mp4",
            "resolution": "hd",
            "aspectRatio": "9:16"  # vertical for TikTok/Reels
        }
    }
    
    try:
        result = shotstack.create_render(timeline)
        return jsonify({'render_id': result['response']['id'], 'status': 'queued'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<render_id>')
def status(render_id):
    try:
        status = shotstack.get_render_status(render_id)
        return jsonify(status['response'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)