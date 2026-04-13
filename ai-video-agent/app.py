import os
import openai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.shotstack_client import ShotstackClient

load_dotenv()
app = Flask(__name__)
shotstack = ShotstackClient()
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    topic = data.get('topic', '').strip()
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    # Use OpenAI to generate a short script
    if openai.api_key:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a scriptwriter. Create a 3-5 sentence video script about the given topic. Keep it engaging."},
                    {"role": "user", "content": topic}
                ],
                max_tokens=150,
                temperature=0.7
            )
            script = response.choices[0].message.content.strip()
        except Exception as e:
            script = f"Explore the amazing world of {topic}. Discover new insights and ideas. Stay tuned for more!"
    else:
        script = f"Learn about {topic}. This video was created automatically by the AI Video Agent."

    # Build timeline
    timeline = {
        "timeline": {
            "background": "#2d2f3b",
            "tracks": [{
                "clips": [{
                    "asset": {
                        "type": "title",
                        "text": script,
                        "style": "minimal",
                        "position": "center"
                    },
                    "start": 0,
                    "length": 8
                }]
            }]
        },
        "output": {
            "format": "mp4",
            "resolution": "hd"
        }
    }

    try:
        result = shotstack.create_render(timeline)
        return jsonify({'render_id': result['response']['id'], 'script': script})
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
