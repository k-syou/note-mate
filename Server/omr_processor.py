"""
OMR (Optical Music Recognition) Processor
Uses oemer library to convert sheet music images to MusicXML
"""
import os
from pathlib import Path
from PIL import Image
import cv2
import numpy as np


class OMRProcessor:
    """
    Handles optical music recognition processing
    """
    
    def __init__(self):
        """Initialize the OMR processor"""
        self.model_loaded = False
        
    def preprocess_image(self, image_path):
        """
        Preprocess the input image for better OMR results
        
        Args:
            image_path (str): Path to the input image
            
        Returns:
            str: Path to the preprocessed image
        """
        try:
            # Read image
            img = cv2.imread(str(image_path))
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply adaptive thresholding for better contrast
            binary = cv2.adaptiveThreshold(
                gray, 255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 
                11, 2
            )
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(binary, None, 10, 7, 21)
            
            # Save preprocessed image
            preprocessed_path = str(image_path).replace('.', '_preprocessed.')
            cv2.imwrite(preprocessed_path, denoised)
            
            return preprocessed_path
            
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            return image_path  # Return original if preprocessing fails
    
    def recognize_score(self, image_path, preprocess=True):
        """
        Recognize sheet music from image and convert to MusicXML
        
        Args:
            image_path (str): Path to the sheet music image
            preprocess (bool): Whether to preprocess the image
            
        Returns:
            tuple: (success: bool, result: str or error_message: str)
        """
        try:
            # Preprocess image if requested
            if preprocess:
                processed_path = self.preprocess_image(image_path)
            else:
                processed_path = image_path
            
            # Import oemer here to avoid loading if not needed
            from oemer import OMR
            
            # Initialize OMR
            omr = OMR(processed_path)
            
            # Run recognition
            musicxml = omr.run()
            
            # Generate output path
            output_path = str(image_path).rsplit('.', 1)[0] + '.musicxml'
            
            # Save MusicXML
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(musicxml)
            
            return True, output_path
            
        except ImportError:
            return False, "OMR library (oemer) not installed. Please install it using: pip install oemer"
        
        except Exception as e:
            return False, f"Error during OMR processing: {str(e)}"
    
    def validate_musicxml(self, musicxml_path):
        """
        Validate the generated MusicXML file
        
        Args:
            musicxml_path (str): Path to the MusicXML file
            
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        try:
            # Check if file exists
            if not Path(musicxml_path).exists():
                return False, "MusicXML file not found"
            
            # Check file size
            file_size = Path(musicxml_path).stat().st_size
            if file_size == 0:
                return False, "MusicXML file is empty"
            
            # Try to parse with music21
            from music21 import converter
            score = converter.parse(musicxml_path)
            
            # Check if score has any notes
            notes = score.flatten().notes
            if len(notes) == 0:
                return False, "No notes found in the score"
            
            return True, f"Valid MusicXML with {len(notes)} notes"
            
        except Exception as e:
            return False, f"Invalid MusicXML: {str(e)}"
    
    def extract_metadata(self, musicxml_path):
        """
        Extract metadata from MusicXML file
        
        Args:
            musicxml_path (str): Path to the MusicXML file
            
        Returns:
            dict: Metadata information
        """
        try:
            from music21 import converter
            
            score = converter.parse(musicxml_path)
            
            metadata = {
                'title': score.metadata.title if score.metadata else 'Untitled',
                'composer': score.metadata.composer if score.metadata else 'Unknown',
                'time_signature': None,
                'key_signature': None,
                'tempo': None,
                'num_measures': len(score.parts[0].getElementsByClass('Measure')) if score.parts else 0,
                'num_notes': len(score.flatten().notes),
                'instruments': []
            }
            
            # Get time signature
            ts = score.flatten().getElementsByClass('TimeSignature')
            if ts:
                metadata['time_signature'] = ts[0].ratioString
            
            # Get key signature
            ks = score.flatten().getElementsByClass('KeySignature')
            if ks:
                metadata['key_signature'] = str(ks[0])
            
            # Get tempo
            tempos = score.flatten().getElementsByClass('MetronomeMark')
            if tempos:
                metadata['tempo'] = tempos[0].number
            
            # Get instruments
            for part in score.parts:
                if part.partName:
                    metadata['instruments'].append(part.partName)
            
            return metadata
            
        except Exception as e:
            return {'error': str(e)}
