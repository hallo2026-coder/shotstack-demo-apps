# 🎬 Shotstack Demo Apps

[![Shotstack](https://img.shields.io/badge/Powered%20by-Shotstack-blue)](https://shotstack.io)
[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Live Demo](https://img.shields.io/badge/demo-online-brightgreen)](https://python-text-to-video.onrender.com)

Three production-ready demo applications showcasing the **Shotstack video editing API** – built as part of a job application for **Developer Advocate** at Shotstack.

## 🚀 Live Demos

| Demo | Description | Live URL |
|------|-------------|----------|
| **Text-to-Video** | Generate a simple video from plain text | [➡️ Try it](https://python-text-to-video.onrender.com) |
| **Social Video Pipeline** | Convert blog posts into vertical TikTok/Reels videos with music | [➡️ Try it](https://social-video-pipeline.onrender.com) |
| **AI Video Agent** | GPT generates a script → Shotstack renders the video | [➡️ Try it](https://ai-video-agent-fw62.onrender.com) |

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Video API**: [Shotstack](https://shotstack.io)
- **AI**: OpenAI GPT-3.5 / Groq Llama (fallback)
- **Deployment**: Render (free tier)

## 📦 Local Setup

### Prerequisites
- Python 3.9+
- Shotstack API key (free trial at [shotstack.io](https://shotstack.io))
- (Optional) OpenAI or Groq API key for AI agent

### 1. Clone & Install
```bash
git clone https://github.com/hallo2026-coder/shotstack-demo-apps.git
cd shotstack-demo-apps

# Install dependencies for each demo (or use a virtual env)
pip install -r text-to-video/requirements.txt
pip install -r social-video-pipeline/requirements.txt
pip install -r ai-video-agent/requirements.txt