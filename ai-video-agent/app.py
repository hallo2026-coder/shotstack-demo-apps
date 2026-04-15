import sys
from pathlib import Path

# Add the parent directory to Python's module search path
# This makes the 'shared' module importable when running on Render
sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from shared.shotstack_client import ShotstackClient
from openai import OpenAI

load_dotenv()
app = Flask(__name__)
shotstack = ShotstackClient()
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')) if os.getenv('OPENAI_API_KEY') else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_script', methods=['POST'])
def generate_script():
    if not openai_client:
        return jsonify({'error': 'OpenAI API key not configured'}), 500
    
    data = request.json
    topic = data.get('topic', '')
    if not topic:
        return jsonify({'error': 'Please provide a topic'}), 400
    
    try:
        # Use GPT to generate a short video script (2-3 sentences per scene)
        prompt = f"""Write a short, engaging video script about "{topic}" with exactly 3 scenes.
        Each scene should be a single sentence (max 15 words). Return only JSON:
        {{"scenes": ["Scene1 text", "Scene2 text", "Scene3 text"]}}"""
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        # Extract JSON (handle markdown code blocks)
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]
        script = json.loads(content)
        return jsonify(script)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/render', methods=['POST'])
def render():
    data = request.json
    scenes = data.get('scenes', [])
    if not scenes:
        return jsonify({'error': 'No scenes provided'}), 400
    
    # Build video timeline from AI-generated script
    clips = []
    start = 0
    duration = 4  # seconds per scene
    for i, scene_text in enumerate(scenes):
        clips.append({
            "asset": {
                "type": "title",
                "text": scene_text,
                "style": "bold",
                "position": "center",
                "background": "#1a1a2e",
                "color": "#e0e0e0"
            },
            "start": start,
            "length": duration,
            "effect": "zoomIn" if i == 0 else "slideRight"
        })
        start += duration
    
    timeline = {
        "timeline": {
            "background": "#1a1a2e",
            "tracks": [{"clips": clips}]
        },
        "output": {
            "format": "mp4",
            "resolution": "hd"
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
    app.run(debug=True, port=5003)