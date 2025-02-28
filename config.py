import os
from dotenv import load_dotenv
import tempfile

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash-lite"  # Changed from "gemini-2.0-flash"

MAX_CONTEXT_LENGTH = 10
ALLOWED_FILE_TYPES = [
    'png', 'jpg', 'jpeg', 'gif', 'bmp',  # Images
    'pdf', 'doc', 'docx', 'txt', 'rtf',   # Documents
    'mp3', 'wav', 'ogg',                  # Audio
    'mp4', 'avi', 'mov', 'mkv'            # Video
]

TEMP_UPLOAD_DIR = tempfile.gettempdir()
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Network Operations Configuration
NETWORK_DEVICES = ['Device X', 'Router Y', 'Switch Z']
NETWORK_METRICS = ['load', 'status', 'uptime']
ISSUE_TYPES = ['connectivity', 'performance']

# Visualization Settings (for future implementation)
CHART_COLORS = {
    'normal': '#28a745',
    'warning': '#ffc107',
    'critical': '#dc3545'
}
