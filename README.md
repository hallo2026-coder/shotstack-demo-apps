# 🎬 Shotstack Demo Apps

[![Shotstack](https://img.shields.io/badge/Powered%20by-Shotstack-blue)](https://shotstack.io)
[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Three production-ready demo applications showcasing the **Shotstack video editing API** – built as part of a job application for **Developer Advocate** at Shotstack.

## 🚀 Demos

| Demo | Description | Port |
|------|-------------|------|
| **Text-to-Video** | Generate a simple video from plain text | 5001 |
| **Social Video Pipeline** | Convert blog posts into vertical TikTok/Reels videos with music | 5002 |
| **AI Video Agent** | GPT generates a script → Shotstack renders the video | 5003 |

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Video API**: [Shotstack](https://shotstack.io)
- **AI**: OpenAI GPT-3.5 (optional for AI agent)
- **Deployment**: Docker / Render / Heroku

## 📦 Local Setup

### Prerequisites
- Python 3.9+
- Shotstack API key (free trial at [shotstack.io](https://shotstack.io))
- (Optional) OpenAI API key for AI agent

### 1. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/shotstack-demo-apps.git
cd shotstack-demo-apps

# Install dependencies for each demo (or use a virtual env)
pip install -r text-to-video/requirements.txt
pip install -r social-video-pipeline/requirements.txt
pip install -r ai-video-agent/requirements.txt