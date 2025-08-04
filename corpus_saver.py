"""
Corpus Saver Module for BhashaBridge
Handles saving audio files, transcriptions, translations, and metadata
Supports export to JSONL, CSV, and ZIP formats
"""

import os
import json
import csv
import zipfile
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
import uuid
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CorpusSaver:
    """Handles corpus data collection and export"""
    
    def __init__(self, corpus_dir: str = "corpus"):
        """
        Initialize corpus saver
        
        Args:
            corpus_dir: Directory to store corpus data
        """
        self.corpus_dir = Path(corpus_dir)
        self.audio_dir = self.corpus_dir / "audio"
        self.metadata_dir = self.corpus_dir / "metadata"
        self.exports_dir = self.corpus_dir / "exports"
        
        # Create directories if they don't exist
        self._create_directories()
        
        # Metadata file paths
        self.metadata_file = self.metadata_dir / "corpus_metadata.jsonl"
        self.feedback_file = self.metadata_dir / "feedback.jsonl"
        
    def _create_directories(self):
        """Create necessary directories"""
        for directory in [self.corpus_dir, self.audio_dir, self.metadata_dir, self.exports_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory ensured: {directory}")
    
    def save_corpus_entry(self, 
                         audio_data: bytes,
                         transcription: str,
                         translation: str,
                         src_lang: str,
                         tgt_lang: str,
                         confidence: float = 0.0,
                         user_id: Optional[str] = None,
                         additional_metadata: Optional[Dict] = None) -> str:
        """
        Save a complete corpus entry
        
        Args:
            audio_data: Raw audio data (bytes)
            transcription: Transcribed text
            translation: Translated text
            src_lang: Source language code
            tgt_lang: Target language code
            confidence: Confidence score (0-1)
            user_id: Optional user identifier
            additional_metadata: Additional metadata dict
            
        Returns:
            Entry ID (UUID)
        """
        try:
            # Generate unique entry ID
            entry_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            
            # Save audio file
            audio_filename = f"{entry_id}.wav"
            audio_path = self.audio_dir / audio_filename
            
            with open(audio_path, 'wb') as f:
                f.write(audio_data)
            
            # Prepare metadata
            metadata = {
                'entry_id': entry_id,
                'timestamp': timestamp,
                'audio_filename': audio_filename,
                'audio_path': str(audio_path),
                'transcription': transcription,
                'translation': translation,
                'src_lang': src_lang,
                'tgt_lang': tgt_lang,
                'confidence': confidence,
                'user_id': user_id,
                'audio_size_bytes': len(audio_data),
                'status': 'pending_feedback'
            }
            
            # Add additional metadata if provided
            if additional_metadata:
                metadata.update(additional_metadata)
            
            # Save metadata to JSONL file
            with open(self.metadata_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(metadata, ensure_ascii=False) + '\n')
            
            logger.info(f"Corpus entry saved: {entry_id}")
            return entry_id
            
        except Exception as e:
            logger.error(f"Failed to save corpus entry: {e}")
            raise
    
    def save_feedback(self, 
                     entry_id: str, 
                     is_correct: bool, 
                     corrected_transcription: Optional[str] = None,
                     corrected_translation: Optional[str] = None,
                     user_comments: Optional[str] = None) -> bool:
        """
        Save user feedback for a corpus entry
        
        Args:
            entry_id: Entry ID to provide feedback for
            is_correct: Whether the transcription/translation is correct
            corrected_transcription: Corrected transcription if wrong
            corrected_translation: Corrected translation if wrong
            user_comments: Additional user comments
            
        Returns:
            Success status
        """
        try:
            feedback_data = {
                'entry_id': entry_id,
                'timestamp': datetime.now().isoformat(),
                'is_correct': is_correct,
                'corrected_transcription': corrected_transcription,
                'corrected_translation': corrected_translation,
                'user_comments': user_comments
            }
            
            # Save feedback
            with open(self.feedback_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(feedback_data, ensure_ascii=False) + '\n')
            
            # Update entry status
            self._update_entry_status(entry_id, 'feedback_received')
            
            logger.info(f"Feedback saved for entry: {entry_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save feedback: {e}")
            return False
    
    def _update_entry_status(self, entry_id: str, new_status: str):
        """Update the status of a corpus entry"""
        try:
            # Read all metadata
            entries = self.load_all_metadata()
            
            # Update the specific entry
            updated_entries = []
            for entry in entries:
                if entry.get('entry_id') == entry_id:
                    entry['status'] = new_status
                    entry['last_updated'] = datetime.now().isoformat()
                updated_entries.append(entry)
            
            # Rewrite metadata file
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                for entry in updated_entries:
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                    
        except Exception as e:
            logger.error(f"Failed to update entry status: {e}")
    
    def load_all_metadata(self) -> List[Dict]:
        """Load all corpus metadata"""
        entries = []
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            entries.append(json.loads(line.strip()))
        except Exception as e:
            logger.error(f"Failed to load metadata: {e}")
        
        return entries
    
    def load_all_feedback(self) -> List[Dict]:
        """Load all feedback data"""
        feedback = []
        try:
            if self.feedback_file.exists():
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            feedback.append(json.loads(line.strip()))
        except Exception as e:
            logger.error(f"Failed to load feedback: {e}")
        
        return feedback
    
    def export_to_csv(self, output_path: Optional[str] = None) -> str:
        """
        Export corpus metadata to CSV
        
        Args:
            output_path: Output CSV file path
            
        Returns:
            Path to exported CSV file
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.exports_dir / f"corpus_export_{timestamp}.csv"
        
        try:
            entries = self.load_all_metadata()
            
            if not entries:
                logger.warning("No corpus entries to export")
                return str(output_path)
            
            # Define CSV headers
            headers = [
                'entry_id', 'timestamp', 'audio_filename', 'transcription', 
                'translation', 'src_lang', 'tgt_lang', 'confidence', 
                'user_id', 'audio_size_bytes', 'status'
            ]
            
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                for entry in entries:
                    # Filter entry to only include CSV headers
                    csv_entry = {key: entry.get(key, '') for key in headers}
                    writer.writerow(csv_entry)
            
            logger.info(f"CSV export completed: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"CSV export failed: {e}")
            raise
    
    def export_to_jsonl(self, output_path: Optional[str] = None) -> str:
        """
        Export corpus metadata to JSONL
        
        Args:
            output_path: Output JSONL file path
            
        Returns:
            Path to exported JSONL file
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.exports_dir / f"corpus_export_{timestamp}.jsonl"
        
        try:
            entries = self.load_all_metadata()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for entry in entries:
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
            logger.info(f"JSONL export completed: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"JSONL export failed: {e}")
            raise
    
    def export_to_zip(self, output_path: Optional[str] = None, include_audio: bool = True) -> str:
        """
        Export entire corpus to ZIP file
        
        Args:
            output_path: Output ZIP file path
            include_audio: Whether to include audio files
            
        Returns:
            Path to exported ZIP file
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.exports_dir / f"corpus_full_export_{timestamp}.zip"
        
        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add metadata files
                if self.metadata_file.exists():
                    zipf.write(self.metadata_file, "metadata/corpus_metadata.jsonl")
                
                if self.feedback_file.exists():
                    zipf.write(self.feedback_file, "metadata/feedback.jsonl")
                
                # Export and add CSV
                csv_path = self.export_to_csv()
                zipf.write(csv_path, f"exports/{Path(csv_path).name}")
                
                # Export and add JSONL
                jsonl_path = self.export_to_jsonl()
                zipf.write(jsonl_path, f"exports/{Path(jsonl_path).name}")
                
                # Add audio files if requested
                if include_audio and self.audio_dir.exists():
                    for audio_file in self.audio_dir.glob("*.wav"):
                        zipf.write(audio_file, f"audio/{audio_file.name}")
                
                # Add README
                readme_content = self._generate_readme()
                zipf.writestr("README.txt", readme_content)
            
            logger.info(f"ZIP export completed: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"ZIP export failed: {e}")
            raise
    
    def _generate_readme(self) -> str:
        """Generate README content for exports"""
        entries = self.load_all_metadata()
        feedback = self.load_all_feedback()
        
        stats = self.get_corpus_stats()
        
        readme = f"""BhashaBridge Corpus Export
Generated: {datetime.now().isoformat()}

CORPUS STATISTICS:
- Total Entries: {stats['total_entries']}
- Total Audio Files: {stats['total_audio_files']}
- Languages: {', '.join(stats['languages'])}
- Total Feedback: {stats['total_feedback']}
- Correct Feedback: {stats['correct_feedback']}

DIRECTORY STRUCTURE:
- audio/: Audio files (.wav format)
- metadata/: Raw metadata files (.jsonl format)
- exports/: Processed exports (.csv and .jsonl)
- README.txt: This file

FILE FORMATS:
- corpus_metadata.jsonl: Complete metadata for all entries
- feedback.jsonl: User feedback data
- corpus_export_*.csv: Tabular format for analysis
- corpus_export_*.jsonl: JSON Lines format for processing

USAGE:
This corpus can be used for:
1. Training speech recognition models
2. Training translation models
3. Evaluating multilingual AI systems
4. Research in Indian language processing

For questions or issues, please refer to the BhashaBridge documentation.
"""
        return readme
    
    def get_corpus_stats(self) -> Dict[str, Any]:
        """Get corpus statistics"""
        entries = self.load_all_metadata()
        feedback = self.load_all_feedback()
        
        # Calculate statistics
        total_entries = len(entries)
        languages = set()
        total_audio_size = 0
        
        for entry in entries:
            languages.add(entry.get('src_lang', ''))
            languages.add(entry.get('tgt_lang', ''))
            total_audio_size += entry.get('audio_size_bytes', 0)
        
        languages.discard('')  # Remove empty strings
        
        # Feedback statistics
        total_feedback = len(feedback)
        correct_feedback = sum(1 for f in feedback if f.get('is_correct', False))
        
        # Audio file count
        audio_files = list(self.audio_dir.glob("*.wav")) if self.audio_dir.exists() else []
        
        return {
            'total_entries': total_entries,
            'total_audio_files': len(audio_files),
            'languages': sorted(list(languages)),
            'total_audio_size_bytes': total_audio_size,
            'total_audio_size_mb': round(total_audio_size / (1024 * 1024), 2),
            'total_feedback': total_feedback,
            'correct_feedback': correct_feedback,
            'accuracy_rate': round(correct_feedback / total_feedback * 100, 2) if total_feedback > 0 else 0
        }
    
    def cleanup_old_exports(self, days_old: int = 7):
        """Clean up old export files"""
        try:
            cutoff_time = datetime.now().timestamp() - (days_old * 24 * 3600)
            
            for export_file in self.exports_dir.glob("*"):
                if export_file.stat().st_mtime < cutoff_time:
                    export_file.unlink()
                    logger.info(f"Cleaned up old export: {export_file}")
                    
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")

# Global instance for easy access
corpus_saver = CorpusSaver()

def save_corpus_entry(audio_data: bytes, transcription: str, translation: str, 
                     src_lang: str, tgt_lang: str, **kwargs) -> str:
    """Simple function to save corpus entry"""
    return corpus_saver.save_corpus_entry(
        audio_data, transcription, translation, src_lang, tgt_lang, **kwargs
    )

def save_feedback(entry_id: str, is_correct: bool, **kwargs) -> bool:
    """Simple function to save feedback"""
    return corpus_saver.save_feedback(entry_id, is_correct, **kwargs)

def export_corpus_zip(include_audio: bool = True) -> str:
    """Simple function to export corpus as ZIP"""
    return corpus_saver.export_to_zip(include_audio=include_audio)

if __name__ == "__main__":
    # Test the module
    saver = CorpusSaver()
    print("Corpus saver module loaded successfully!")
    print(f"Corpus directory: {saver.corpus_dir}")
    
    # Display current stats
    stats = saver.get_corpus_stats()
    print(f"Current corpus stats: {stats}")
