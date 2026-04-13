import re
import hashlib
from typing import List, Dict, Any

def sanitize_filename(text: str, max_len: int = 50) -> str:
    """Convert text to safe filename"""
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text[:max_len]

def generate_thumbhash(video_url: str) -> str:
    """Placeholder for generating thumbhash from video (optional)"""
    # In real implementation, you'd download & process video
    return hashlib.md5(video_url.encode()).hexdigest()[:8]

def chunk_text_for_scenes(text: str, max_chars_per_scene: int = 280) -> List[str]:
    """Split long text into scenes for multi-clip videos"""
    words = text.split()
    scenes = []
    current = []
    current_len = 0
    
    for word in words:
        if current_len + len(word) + 1 > max_chars_per_scene and current:
            scenes.append(' '.join(current))
            current = [word]
            current_len = len(word)
        else:
            current.append(word)
            current_len += len(word) + 1
    
    if current:
        scenes.append(' '.join(current))
    
    return scenes if scenes else [text]