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
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    # Build a simple timeline: title clip with background color
    timeline = {
        "timeline": {
            "background": "#000000",
            "tracks": [{
                "clips": [{
                    "asset": {
                        "type": "title",
                        "text": text,
                        "style": "minimal",
                        "position": "center"
                    },
                    "start": 0,
                    "length": 5
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
        render_id = result['response']['id']
        return jsonify({'render_id': render_id, 'status': 'queued'})
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
    app.run(debug=True, port=5001)
