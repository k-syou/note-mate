"""
Configuration settings for the AI Music Score Service
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Upload settings
UPLOAD_FOLDER = BASE_DIR / 'uploads'
OUTPUT_FOLDER = BASE_DIR / 'outputs'
TEMP_FOLDER = BASE_DIR / 'temp'

# Create directories if they don't exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)
TEMP_FOLDER.mkdir(exist_ok=True)

# File settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# OMR settings
OMR_MODEL_PATH = BASE_DIR / 'models' / 'oemer'
OMR_CONFIDENCE_THRESHOLD = 0.5

# Music processing settings
DEFAULT_TEMPO = 120  # BPM
TEMPO_RANGE = (50, 200)  # Min and max tempo
SIMPLIFICATION_LEVELS = {
    'easy': {
        'tempo_factor': 0.7,
        'simplify_rhythm': True,
        'simplify_chords': True,
        'remove_ornaments': True
    },
    'medium': {
        'tempo_factor': 0.85,
        'simplify_rhythm': True,
        'simplify_chords': False,
        'remove_ornaments': True
    },
    'original': {
        'tempo_factor': 1.0,
        'simplify_rhythm': False,
        'simplify_chords': False,
        'remove_ornaments': False
    }
}

# Supported instruments
SUPPORTED_INSTRUMENTS = ['piano', 'guitar']

# Flask settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))

# CORS settings
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
