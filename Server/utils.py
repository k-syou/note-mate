"""
Utility functions for file handling, validation, and error management
"""
import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE


def allowed_file(filename):
    """
    Check if the file extension is allowed
    
    Args:
        filename (str): Name of the file
        
    Returns:
        bool: True if extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file_size(file_size):
    """
    Validate file size against maximum allowed size
    
    Args:
        file_size (int): Size of the file in bytes
        
    Returns:
        bool: True if size is valid, False otherwise
    """
    return file_size <= MAX_FILE_SIZE


def generate_unique_filename(original_filename):
    """
    Generate a unique filename while preserving the extension
    
    Args:
        original_filename (str): Original filename
        
    Returns:
        str: Unique filename
    """
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{ext}" if ext else unique_id


def save_uploaded_file(file, upload_folder):
    """
    Save uploaded file with a unique filename
    
    Args:
        file: FileStorage object from Flask
        upload_folder (Path): Directory to save the file
        
    Returns:
        tuple: (success: bool, filepath: str or error_message: str)
    """
    try:
        if not file:
            return False, "No file provided"
        
        if not allowed_file(file.filename):
            return False, f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        
        # Generate unique filename
        filename = generate_unique_filename(file.filename)
        filepath = upload_folder / filename
        
        # Save file
        file.save(str(filepath))
        
        # Validate size after saving
        if not validate_file_size(filepath.stat().st_size):
            filepath.unlink()  # Delete the file
            return False, f"File size exceeds maximum allowed size ({MAX_FILE_SIZE / (1024*1024)}MB)"
        
        return True, str(filepath)
    
    except Exception as e:
        return False, f"Error saving file: {str(e)}"


def cleanup_temp_files(directory, max_age_hours=24):
    """
    Clean up temporary files older than specified hours
    
    Args:
        directory (Path): Directory to clean
        max_age_hours (int): Maximum age of files in hours
    """
    import time
    
    try:
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for filepath in directory.iterdir():
            if filepath.is_file():
                file_age = current_time - filepath.stat().st_mtime
                if file_age > max_age_seconds:
                    filepath.unlink()
                    
    except Exception as e:
        print(f"Error cleaning up temp files: {str(e)}")


def create_error_response(message, status_code=400):
    """
    Create a standardized error response
    
    Args:
        message (str): Error message
        status_code (int): HTTP status code
        
    Returns:
        tuple: (response_dict, status_code)
    """
    return {
        'success': False,
        'error': message
    }, status_code


def create_success_response(data, message="Success"):
    """
    Create a standardized success response
    
    Args:
        data (dict): Response data
        message (str): Success message
        
    Returns:
        dict: Response dictionary
    """
    return {
        'success': True,
        'message': message,
        'data': data
    }
