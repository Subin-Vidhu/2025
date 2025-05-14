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
        # Check file size first - if too small, may indicate an empty or corrupted file
        file_size = os.path.getsize(input_file)
        if file_size < 100:  # Extremely small file
            logger.warning(f"File too small to be valid audio: {input_file} ({file_size} bytes)")
            return input_file
        
        # Check if input file is already in the correct format
        try:
            info = get_audio_info(input_file)
            # If already in the correct format, return the original file
            if (info.get('codec') == target_format or
                (target_format == 'wav' and info.get('codec') == 'pcm_s16le')) and \
               info.get('sample_rate') == sample_rate and \
               info.get('channels') == channels:
                logger.info(f"Audio file {input_file} already in required format")
                return input_file
        except Exception as e:
            logger.warning(f"Error getting audio info: {e}. Will attempt conversion anyway.")
            
        # Create temporary output file
        output_fd, output_path = tempfile.mkstemp(suffix=f".{target_format}")
        os.close(output_fd)
        
        # Build ffmpeg command with more robust options for browser-captured audio
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-ar", str(sample_rate),
            "-ac", str(channels),
            "-y",  # Overwrite output file if it exists
            "-f", target_format,  # Force output format
            "-acodec", "pcm_s16le",  # Use standard PCM encoding for WAV
            "-loglevel", "warning",  # Reduce log noise but keep warnings
            output_path
        ]
        
        # Run ffmpeg with full output capture for debugging
        process = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Check if the process was successful
        if process.returncode != 0:
            logger.error(f"Failed to convert audio file: {process.stderr}")
            # If the output file was created but is invalid or empty, remove it
            if os.path.exists(output_path) and os.path.getsize(output_path) < 100:  # Very small file is likely invalid
                os.unlink(output_path)
            # Return the original file if conversion fails
            if os.path.exists(input_file):
                return input_file
            return None
        
        # Verify the output file exists and has reasonable size
        if os.path.exists(output_path) and os.path.getsize(output_path) > 100:
            logger.info(f"Successfully converted audio file: {input_file} -> {output_path}")
            return output_path
        else:
            logger.error(f"Conversion produced invalid or empty file: {output_path}")
            # Clean up empty/invalid output file
            if os.path.exists(output_path):
                os.unlink(output_path)
            # Return the original file as fallback
            return input_file
        
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
    # If file doesn't exist, return error info
    if not os.path.exists(file_path):
        logger.warning(f"Cannot get audio info - file not found: {file_path}")
        return {"error": f"File not found: {file_path}"}
    
    # Get basic file stats regardless of ffmpeg availability
    basic_info = {
        "file_path": file_path,
        "file_size": os.path.getsize(file_path),
    }
    
    # If ffmpeg is not available, check for basic WAV header
    if not FFMPEG_AVAILABLE:
        basic_info["note"] = "Limited info available without ffmpeg"
        try:
            with open(file_path, 'rb') as f:
                header = f.read(44)  # Read WAV header (minimum 44 bytes)
                if len(header) >= 44 and header[0:4] == b'RIFF' and header[8:12] == b'WAVE':
                    # Extract basic info from WAV header
                    channels = int.from_bytes(header[22:24], byteorder='little')
                    sample_rate = int.from_bytes(header[24:28], byteorder='little')
                    bits_per_sample = int.from_bytes(header[34:36], byteorder='little') if len(header) >= 36 else 0
                    
                    basic_info.update({
                        "codec": "wav",
                        "channels": channels,
                        "sample_rate": sample_rate,
                        "bits_per_sample": bits_per_sample
                    })
                    logger.debug(f"Extracted basic WAV info: {channels} channels, {sample_rate} Hz")
                else:
                    basic_info["warning"] = "Not a valid WAV file or header cannot be read"
        except Exception as e:
            logger.error(f"Error reading file header: {e}")
            basic_info["error"] = f"Error reading file header: {str(e)}"
        
        return basic_info
    
    # Use ffprobe for detailed information
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "stream=codec_name,codec_type,channels,sample_rate,bit_rate:format=duration",
            "-of", "json",
            file_path
        ]
        
        process = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        if process.returncode != 0:
            logger.error(f"FFprobe error: {process.stderr}")
            basic_info["error"] = f"FFprobe error: {process.stderr}"
            return basic_info
        
        import json
        result = json.loads(process.stdout)
        
        # Extract relevant information
        audio_info = basic_info.copy()
        
        # Add format info if available
        if "format" in result:
            fmt = result["format"]
            audio_info.update({
                "duration": float(fmt.get("duration", 0)),
                "format": fmt.get("format_name", "unknown"),
                "bit_rate": int(fmt.get("bit_rate", 0)) if "bit_rate" in fmt else None
            })
        
        # Add stream info if available
        if "streams" in result and result["streams"]:
            # Find the audio stream
            audio_streams = [s for s in result["streams"] if s.get("codec_type") == "audio"]
            if audio_streams:
                stream = audio_streams[0]
                audio_info.update({
                    "codec": stream.get("codec_name", "unknown"),
                    "channels": int(stream.get("channels", 0)),
                    "sample_rate": int(stream.get("sample_rate", 0)),
                    "bit_rate": int(stream.get("bit_rate", 0)) if "bit_rate" in stream else None
                })
            else:
                audio_info["warning"] = "No audio stream found"
                
        return audio_info
        
    except Exception as e:
        logger.error(f"Error getting audio info: {str(e)}")
        basic_info["error"] = str(e)
        return basic_info 