import os
import time
import requests
from typing import Dict, Any, Optional

class ShotstackClient:
    """Simple wrapper for Shotstack API"""

    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv('SHOTSTACK_API_KEY')
        self.base_url = base_url or os.getenv('SHOTSTACK_API_URL', 'https://api.shotstack.io')
        if not self.api_key:
            raise ValueError("SHOTSTACK_API_KEY is required")
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        })

    def create_render(self, timeline: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a render job"""
        response = self.session.post(f"{self.base_url}/render", json=timeline)
        response.raise_for_status()
        return response.json()

    def get_render_status(self, render_id: str) -> Dict[str, Any]:
        """Check render status"""
        response = self.session.get(f"{self.base_url}/render/{render_id}")
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, render_id: str, timeout: int = 300, poll_interval: int = 2) -> Dict[str, Any]:
        """Poll until render completes"""
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_render_status(render_id)
            if status['response']['status'] in ('done', 'failed'):
                return status
            time.sleep(poll_interval)
        raise TimeoutError(f"Render {render_id} did not complete within {timeout}s")
