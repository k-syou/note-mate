"""
Flask Application for AI Music Score Service
Main API endpoints for sheet music processing
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
import traceback

from config import *
from utils import (
    save_uploaded_file, 
    create_error_response, 
    create_success_response,
    cleanup_temp_files
)
from omr_processor import OMRProcessor
from music_processor import MusicProcessor

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Enable CORS
CORS(app, origins=CORS_ORIGINS)

# Initialize processors
omr_processor = OMRProcessor()
music_processor = MusicProcessor()

# Store processing results (in production, use a database)
processing_cache = {}


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'service': 'AI Music Score Service',
        'version': '1.0.0',
        'endpoints': {
            'upload': '/api/upload',
            'recognize': '/api/recognize',
            'simplify': '/api/simplify',
            'convert': '/api/convert',
            'download': '/api/download/<file_id>'
        }
    })


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Upload a sheet music image
    
    Expected: multipart/form-data with 'file' field
    Returns: file_id for further processing
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return create_error_response('No file provided')
        
        file = request.files['file']
        
        if file.filename == '':
            return create_error_response('No file selected')
        
        # Save the uploaded file
        success, result = save_uploaded_file(file, UPLOAD_FOLDER)
        
        if not success:
            return create_error_response(result)
        
        # Generate file ID
        file_id = Path(result).stem
        
        # Store file info
        processing_cache[file_id] = {
            'original_image': result,
            'status': 'uploaded'
        }
        
        return jsonify(create_success_response({
            'file_id': file_id,
            'filename': file.filename
        }, 'File uploaded successfully'))
    
    except Exception as e:
        print(f"Upload error: {traceback.format_exc()}")
        return create_error_response(f'Upload failed: {str(e)}', 500)


@app.route('/api/recognize', methods=['POST'])
def recognize_score():
    """
    Recognize sheet music from uploaded image
    
    Expected JSON: { "file_id": "...", "preprocess": true/false }
    Returns: MusicXML file path and metadata
    """
    try:
        data = request.get_json()
        
        if not data or 'file_id' not in data:
            return create_error_response('file_id is required')
        
        file_id = data['file_id']
        preprocess = data.get('preprocess', True)
        
        # Check if file exists in cache
        if file_id not in processing_cache:
            return create_error_response('File not found. Please upload first.')
        
        image_path = processing_cache[file_id]['original_image']
        
        # Run OMR
        success, result = omr_processor.recognize_score(image_path, preprocess)
        
        if not success:
            return create_error_response(result)
        
        # Validate MusicXML
        is_valid, validation_msg = omr_processor.validate_musicxml(result)
        
        if not is_valid:
            return create_error_response(f'Recognition failed: {validation_msg}')
        
        # Extract metadata
        metadata = omr_processor.extract_metadata(result)
        
        # Update cache
        processing_cache[file_id].update({
            'musicxml_path': result,
            'status': 'recognized',
            'metadata': metadata
        })
        
        return jsonify(create_success_response({
            'file_id': file_id,
            'musicxml_path': result,
            'metadata': metadata,
            'validation': validation_msg
        }, 'Sheet music recognized successfully'))
    
    except Exception as e:
        print(f"Recognition error: {traceback.format_exc()}")
        return create_error_response(f'Recognition failed: {str(e)}', 500)


@app.route('/api/simplify', methods=['POST'])
def simplify_score():
    """
    Simplify the recognized score
    
    Expected JSON: { "file_id": "...", "level": "easy/medium/original" }
    Returns: Simplified MusicXML and MIDI paths
    """
    try:
        data = request.get_json()
        
        if not data or 'file_id' not in data:
            return create_error_response('file_id is required')
        
        file_id = data['file_id']
        level = data.get('level', 'easy')
        
        # Check if file exists and is recognized
        if file_id not in processing_cache:
            return create_error_response('File not found')
        
        if 'musicxml_path' not in processing_cache[file_id]:
            return create_error_response('Please recognize the score first')
        
        musicxml_path = processing_cache[file_id]['musicxml_path']
        
        # Load score
        score = music_processor.load_score(musicxml_path)
        
        # Simplify score
        simplified_score = music_processor.simplify_score(score, level)
        
        # Save simplified MusicXML
        simplified_xml_path = OUTPUT_FOLDER / f"{file_id}_simplified_{level}.musicxml"
        success, result = music_processor.to_musicxml(simplified_score, str(simplified_xml_path))
        
        if not success:
            return create_error_response(result)
        
        # Convert to MIDI
        midi_path = OUTPUT_FOLDER / f"{file_id}_simplified_{level}.mid"
        success, midi_result = music_processor.to_midi(simplified_score, str(midi_path))
        
        if not success:
            return create_error_response(midi_result)
        
        # Get score info
        score_info = music_processor.get_score_info(simplified_score)
        
        # Update cache
        processing_cache[file_id].update({
            f'simplified_{level}_xml': str(simplified_xml_path),
            f'simplified_{level}_midi': str(midi_path),
            'status': 'simplified'
        })
        
        return jsonify(create_success_response({
            'file_id': file_id,
            'level': level,
            'musicxml_path': str(simplified_xml_path),
            'midi_path': str(midi_path),
            'score_info': score_info
        }, f'Score simplified to {level} level'))
    
    except Exception as e:
        print(f"Simplification error: {traceback.format_exc()}")
        return create_error_response(f'Simplification failed: {str(e)}', 500)


@app.route('/api/convert', methods=['POST'])
def convert_to_midi():
    """
    Convert recognized score to MIDI without simplification
    
    Expected JSON: { "file_id": "..." }
    Returns: MIDI file path
    """
    try:
        data = request.get_json()
        
        if not data or 'file_id' not in data:
            return create_error_response('file_id is required')
        
        file_id = data['file_id']
        
        # Check if file exists and is recognized
        if file_id not in processing_cache:
            return create_error_response('File not found')
        
        if 'musicxml_path' not in processing_cache[file_id]:
            return create_error_response('Please recognize the score first')
        
        musicxml_path = processing_cache[file_id]['musicxml_path']
        
        # Load score
        score = music_processor.load_score(musicxml_path)
        
        # Convert to MIDI
        midi_path = OUTPUT_FOLDER / f"{file_id}_original.mid"
        success, result = music_processor.to_midi(score, str(midi_path))
        
        if not success:
            return create_error_response(result)
        
        # Update cache
        processing_cache[file_id]['original_midi'] = str(midi_path)
        
        return jsonify(create_success_response({
            'file_id': file_id,
            'midi_path': str(midi_path)
        }, 'Converted to MIDI successfully'))
    
    except Exception as e:
        print(f"Conversion error: {traceback.format_exc()}")
        return create_error_response(f'Conversion failed: {str(e)}', 500)


@app.route('/api/download/<file_id>/<file_type>', methods=['GET'])
def download_file(file_id, file_type):
    """
    Download processed files
    
    file_type: musicxml, midi, simplified_easy, simplified_medium, etc.
    """
    try:
        if file_id not in processing_cache:
            return create_error_response('File not found', 404)
        
        file_data = processing_cache[file_id]
        
        # Determine which file to download
        file_path = None
        
        if file_type == 'musicxml':
            file_path = file_data.get('musicxml_path')
        elif file_type == 'midi':
            file_path = file_data.get('original_midi')
        elif file_type.startswith('simplified_'):
            level = file_type.split('_')[1]
            file_path = file_data.get(f'simplified_{level}_midi')
        
        if not file_path or not Path(file_path).exists():
            return create_error_response('Requested file not found', 404)
        
        return send_file(file_path, as_attachment=True)
    
    except Exception as e:
        print(f"Download error: {traceback.format_exc()}")
        return create_error_response(f'Download failed: {str(e)}', 500)


@app.route('/api/status/<file_id>', methods=['GET'])
def get_status(file_id):
    """Get processing status for a file"""
    if file_id not in processing_cache:
        return create_error_response('File not found', 404)
    
    return jsonify(create_success_response({
        'file_id': file_id,
        'status': processing_cache[file_id].get('status', 'unknown'),
        'metadata': processing_cache[file_id].get('metadata', {})
    }))


@app.before_request
def cleanup_old_files():
    """Clean up old temporary files before each request"""
    cleanup_temp_files(TEMP_FOLDER, max_age_hours=24)
    cleanup_temp_files(UPLOAD_FOLDER, max_age_hours=48)


@app.errorhandler(413)
def file_too_large(e):
    """Handle file too large error"""
    return create_error_response(
        f'File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024)}MB',
        413
    )


@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    return create_error_response('Internal server error', 500)


if __name__ == '__main__':
    print(f"""
    ╔══════════════════════════════════════════╗
    ║   🎵 AI Music Score Service Started     ║
    ╠══════════════════════════════════════════╣
    ║   Host: {HOST:<30} ║
    ║   Port: {PORT:<30} ║
    ║   Debug: {str(DEBUG):<29} ║
    ╚══════════════════════════════════════════╝
    """)
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
