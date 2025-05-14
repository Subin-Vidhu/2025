import tempfile
import os
import logging
from pathlib import Path
from typing import Optional
import subprocess
import shutil

logger = logging.getLogger(__name__)

# Check if ffmpeg is installed
FFMPEG_AVAILABLE = bool(shutil.which("ffmpeg"))
if not FFMPEG_AVAILABLE:
    logger.warning("ffmpeg not found in PATH. Audio conversion features will be limited.")

def ensure_required_format(input_file: str, target_format: str = "wav", sample_rate: int = 16000, channels: int = 1) -> Optional[str]:
    """
    Converts an audio file to the required format using ffmpeg
    
    Args:
        input_file: Path to the input audio file
        target_format: Target audio format (default: wav)
        sample_rate: Target sample rate in Hz (default: 16000)
        channels: Target number of audio channels (default: 1, mono)
        
    Returns:
        Path to the converted audio file or None if conversion failed
    """
    # If ffmpeg is not available or the file doesn't exist, return the original file
    if not FFMPEG_AVAILABLE or not os.path.exists(input_file):
        logger.warning(f"Cannot convert audio - ffmpeg not available or file not found: {input_file}")
        if os.path.exists(input_file):
            return input_file
        return None
    
    try:
        # Create temporary output file
        output_fd, output_path = tempfile.mkstemp(suffix=f".{target_format}")
        os.close(output_fd)
        
        # Build ffmpeg command
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-ar", str(sample_rate),
            "-ac", str(channels),
            "-y",  # Overwrite output file if it exists
            output_path
        ]
        
        # Run ffmpeg
        process = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        logger.info(f"Successfully converted audio file: {input_file} -> {output_path}")
        return output_path
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to convert audio file: {e.stderr}")
        # Return the original file if conversion fails
        if os.path.exists(input_file):
            return input_file
        return None
    except Exception as e:
        logger.error(f"Error converting audio file: {str(e)}")
        # Return the original file if conversion fails
        if os.path.exists(input_file):
            return input_file
        return None

def merge_audio_chunks(chunk_files: list[str], output_file: str) -> bool:
    """
    Merges multiple audio chunk files into a single file
    
    Args:
        chunk_files: List of audio chunk file paths
        output_file: Path to the output audio file
        
    Returns:
        True if successful, False otherwise
    """
    # If ffmpeg is not available, we can't merge audio
    if not FFMPEG_AVAILABLE:
        logger.warning("Cannot merge audio chunks - ffmpeg not available")
        return False
    
    try:
        # Create a temporary file listing all chunks
        list_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt')
        for chunk in chunk_files:
            if os.path.exists(chunk):
                list_file.write(f"file '{os.path.abspath(chunk)}'\n")
        list_file.close()
        
        # Build ffmpeg command
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file.name,
            "-c", "copy",
            "-y",  # Overwrite output file if it exists
            output_file
        ]
        
        # Run ffmpeg
        process = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        # Clean up the temporary list file
        os.unlink(list_file.name)
        
        logger.info(f"Successfully merged {len(chunk_files)} audio chunks into {output_file}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to merge audio chunks: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error merging audio chunks: {str(e)}")
        return False
        
def get_audio_info(file_path: str) -> dict:
    """
    Get information about an audio file using ffprobe
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Dictionary with audio information
    """
    # If ffmpeg is not available or the file doesn't exist, return basic info
    if not FFMPEG_AVAILABLE or not os.path.exists(file_path):
        logger.warning(f"Cannot get audio info - ffmpeg not available or file not found: {file_path}")
        if os.path.exists(file_path):
            return {
                "file_path": file_path,
                "file_size": os.path.getsize(file_path),
                "note": "Limited info available without ffmpeg"
            }
        return {"error": f"File not found: {file_path}"}
    
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "stream=codec_name,channels,sample_rate:format=duration",
            "-of", "json",
            file_path
        ]
        
        process = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        import json
        result = json.loads(process.stdout)
        
        # Extract relevant information
        audio_info = {
            "file_path": file_path,
            "file_size": os.path.getsize(file_path),
            "duration": float(result["format"].get("duration", 0)),
        }
        
        # Add stream info if available
        if "streams" in result and result["streams"]:
            stream = result["streams"][0]
            audio_info.update({
                "codec": stream.get("codec_name", "unknown"),
                "channels": int(stream.get("channels", 0)),
                "sample_rate": int(stream.get("sample_rate", 0))
            })
            
        return audio_info
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get audio info: {e.stderr}")
        return {
            "file_path": file_path,
            "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Error getting audio info: {str(e)}")
        return {
            "file_path": file_path, 
            "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            "error": str(e)
        } 