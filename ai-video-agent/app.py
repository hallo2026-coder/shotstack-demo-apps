import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import os, json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from shared.shotstack_client import ShotstackClient

# Import both libraries
from openai import OpenAI
from groq import Groq

load_dotenv()
app = Flask(__name__)
shotstack = ShotstackClient()

# Initialize clients for both providers
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')) if os.getenv('OPENAI_API_KEY') else None
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY')) if os.getenv('GROQ_API_KEY') else None

def generate_script_with_fallback(topic):
    """Try OpenAI first, fall back to Groq if needed."""
    prompt = f"""Write a short, engaging video script about "{topic}" with exactly 3 scenes.
    Each scene should be a single sentence (max 15 words). Return only JSON:
    {{"scenes": ["Scene1 text", "Scene2 text", "Scene3 text"]}}"""

    # Try OpenAI first
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI failed: {e}")

    # Fallback to Groq if OpenAI fails or isn't configured
    if groq_client:
        try:
            print("Falling back to Groq...")
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",  # A fast, capable model on Groq's free tier
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq also failed: {e}")

    # If both fail, raise an exception
    raise Exception("All LLM providers failed.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_script', methods=['POST'])
def generate_script():
    data = request.json
    topic = data.get('topic', '')
    if not topic:
        return jsonify({'error': 'Please provide a topic'}), 400
    
    try:
        # Use the fallback function
        content = generate_script_with_fallback(topic)
        
        # Clean and parse the JSON response
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
    port = int(os.environ.get('PORT', 5003))
    app.run(debug=True, host='0.0.0.0', port=port)