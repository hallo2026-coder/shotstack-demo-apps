import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.shotstack_client import ShotstackClient

load_dotenv()
app = Flask(__name__)
shotstack = ShotstackClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/render', methods=['POST'])
def render():
    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    # Build a simple video with title and scrolling text
    timeline = {
        "timeline": {
            "background": "#1a1a2e",
            "tracks": [{
                "clips": [
                    {
                        "asset": {
                            "type": "title",
                            "text": title,
                            "style": "minimal",
                            "position": "top"
                        },
                        "start": 0,
                        "length": 3
                    },
                    {
                        "asset": {
                            "type": "title",
                            "text": content[:200],
                            "style": "minimal",
                            "position": "center"
                        },
                        "start": 3,
                        "length": 5
                    }
                ]
            }]
        },
        "output": {
            "format": "mp4",
            "resolution": "hd"
        }
    }

    try:
        result = shotstack.create_render(timeline)
        return jsonify({'render_id': result['response']['id']})
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
