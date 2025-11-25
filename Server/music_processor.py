"""
Music Processing Module
Handles music manipulation, simplification, and conversion
"""
from music21 import converter, stream, note, chord, tempo, meter
from pathlib import Path
import copy


class MusicProcessor:
    """
    Handles music processing operations like simplification and conversion
    """
    
    def __init__(self):
        """Initialize the music processor"""
        pass
    
    def load_score(self, musicxml_path):
        """
        Load a MusicXML file
        
        Args:
            musicxml_path (str): Path to the MusicXML file
            
        Returns:
            music21.stream.Score: Parsed score object
        """
        try:
            return converter.parse(musicxml_path)
        except Exception as e:
            raise Exception(f"Error loading score: {str(e)}")
    
    def simplify_rhythm(self, score, factor=2):
        """
        Simplify rhythm by converting shorter notes to longer ones
        
        Args:
            score: music21 Score object
            factor (int): Simplification factor (2 = double note durations)
            
        Returns:
            music21.stream.Score: Simplified score
        """
        try:
            simplified = copy.deepcopy(score)
            
            for part in simplified.parts:
                for element in part.flatten().notesAndRests:
                    # Double the duration
                    element.quarterLength *= factor
            
            return simplified
            
        except Exception as e:
            print(f"Error simplifying rhythm: {str(e)}")
            return score
    
    def simplify_chords(self, score):
        """
        Simplify complex chords to basic triads
        
        Args:
            score: music21 Score object
            
        Returns:
            music21.stream.Score: Simplified score
        """
        try:
            simplified = copy.deepcopy(score)
            
            for part in simplified.parts:
                for element in part.flatten().getElementsByClass(chord.Chord):
                    # Keep only the root, third, and fifth if available
                    if len(element.pitches) > 3:
                        # Get root position chord
                        root_chord = element.root()
                        third = element.third
                        fifth = element.fifth
                        
                        # Create simplified chord
                        new_pitches = [p for p in [root_chord, third, fifth] if p is not None]
                        if new_pitches:
                            element.pitches = new_pitches[:3]
            
            return simplified
            
        except Exception as e:
            print(f"Error simplifying chords: {str(e)}")
            return score
    
    def adjust_tempo(self, score, tempo_factor=1.0):
        """
        Adjust the tempo of the score
        
        Args:
            score: music21 Score object
            tempo_factor (float): Tempo multiplier (0.5 = half speed, 2.0 = double speed)
            
        Returns:
            music21.stream.Score: Score with adjusted tempo
        """
        try:
            adjusted = copy.deepcopy(score)
            
            # Find existing tempo markings
            tempos = adjusted.flatten().getElementsByClass(tempo.MetronomeMark)
            
            if tempos:
                # Adjust existing tempos
                for t in tempos:
                    t.number = int(t.number * tempo_factor)
            else:
                # Add a default tempo
                default_tempo = tempo.MetronomeMark(number=int(120 * tempo_factor))
                adjusted.insert(0, default_tempo)
            
            return adjusted
            
        except Exception as e:
            print(f"Error adjusting tempo: {str(e)}")
            return score
    
    def remove_ornaments(self, score):
        """
        Remove ornaments (trills, mordents, etc.) from the score
        
        Args:
            score: music21 Score object
            
        Returns:
            music21.stream.Score: Score without ornaments
        """
        try:
            cleaned = copy.deepcopy(score)
            
            for part in cleaned.parts:
                # Remove expressions (ornaments, articulations)
                for element in part.flatten().notesAndRests:
                    element.expressions = []
                    element.articulations = []
            
            return cleaned
            
        except Exception as e:
            print(f"Error removing ornaments: {str(e)}")
            return score
    
    def simplify_score(self, score, level='easy'):
        """
        Apply multiple simplification techniques based on difficulty level
        
        Args:
            score: music21 Score object
            level (str): Difficulty level ('easy', 'medium', 'original')
            
        Returns:
            music21.stream.Score: Simplified score
        """
        from config import SIMPLIFICATION_LEVELS
        
        if level not in SIMPLIFICATION_LEVELS:
            level = 'original'
        
        settings = SIMPLIFICATION_LEVELS[level]
        result = copy.deepcopy(score)
        
        # Apply tempo adjustment
        result = self.adjust_tempo(result, settings['tempo_factor'])
        
        # Apply rhythm simplification
        if settings['simplify_rhythm']:
            result = self.simplify_rhythm(result, factor=2)
        
        # Apply chord simplification
        if settings['simplify_chords']:
            result = self.simplify_chords(result)
        
        # Remove ornaments
        if settings['remove_ornaments']:
            result = self.remove_ornaments(result)
        
        return result
    
    def to_midi(self, score, output_path):
        """
        Convert score to MIDI file
        
        Args:
            score: music21 Score object
            output_path (str): Path to save MIDI file
            
        Returns:
            tuple: (success: bool, filepath: str or error_message: str)
        """
        try:
            # Write MIDI file
            score.write('midi', fp=output_path)
            return True, output_path
            
        except Exception as e:
            return False, f"Error converting to MIDI: {str(e)}"
    
    def to_musicxml(self, score, output_path):
        """
        Save score as MusicXML file
        
        Args:
            score: music21 Score object
            output_path (str): Path to save MusicXML file
            
        Returns:
            tuple: (success: bool, filepath: str or error_message: str)
        """
        try:
            # Write MusicXML file
            score.write('musicxml', fp=output_path)
            return True, output_path
            
        except Exception as e:
            return False, f"Error saving MusicXML: {str(e)}"
    
    def get_score_info(self, score):
        """
        Extract information from the score
        
        Args:
            score: music21 Score object
            
        Returns:
            dict: Score information
        """
        try:
            info = {
                'num_parts': len(score.parts),
                'num_measures': 0,
                'num_notes': len(score.flatten().notes),
                'duration': score.duration.quarterLength,
                'time_signatures': [],
                'key_signatures': [],
                'tempos': []
            }
            
            # Count measures
            if score.parts:
                info['num_measures'] = len(score.parts[0].getElementsByClass('Measure'))
            
            # Get time signatures
            for ts in score.flatten().getElementsByClass(meter.TimeSignature):
                info['time_signatures'].append(ts.ratioString)
            
            # Get key signatures
            for ks in score.flatten().getElementsByClass('KeySignature'):
                info['key_signatures'].append(str(ks))
            
            # Get tempos
            for t in score.flatten().getElementsByClass(tempo.MetronomeMark):
                info['tempos'].append(t.number)
            
            return info
            
        except Exception as e:
            return {'error': str(e)}
