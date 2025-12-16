#!/usr/bin/env python3
"""
Script to create an MP4 video from images in the arabic-plates directory.
"""
import os
import subprocess
from pathlib import Path

def create_video_from_images(
    input_dir: str = "arabic_plates",
    output_file: str = "arabic_plates_video.mp4",
    fps: int = 2,
    resolution: str = "1280x720"
):
    """
    Create an MP4 video from JPG images in a directory.
    
    Args:
        input_dir: Directory containing the images
        output_file: Output video filename
        fps: Frames per second (default: 2, meaning each image shows for 0.5 seconds)
        resolution: Video resolution (default: 1280x720)
    """
    # Get the script directory
    script_dir = Path(__file__).parent
    input_path = script_dir / input_dir
    output_path = script_dir / output_file
    
    # Check if input directory exists
    if not input_path.exists():
        print(f"Error: Directory '{input_path}' does not exist")
        return False
    
    # Get all JPG files and sort them
    image_files = sorted(input_path.glob("*.jpg"))
    
    if not image_files:
        print(f"Error: No JPG files found in '{input_path}'")
        return False
    
    print(f"Found {len(image_files)} images")
    print(f"Creating video at {fps} FPS (each image displays for {1/fps:.2f} seconds)")
    
    # Create a temporary file list for ffmpeg
    filelist_path = script_dir / "filelist.txt"
    
    try:
        # Write the file list
        with open(filelist_path, 'w') as f:
            for img in image_files:
                # Use absolute paths and escape single quotes
                abs_path = img.absolute()
                f.write(f"file '{abs_path}'\n")
                f.write(f"duration {1/fps}\n")
            # Add the last image again without duration to hold the last frame
            f.write(f"file '{image_files[-1].absolute()}'\n")
        
        # Build ffmpeg command
        # -f concat: use concat demuxer
        # -safe 0: allow absolute paths
        # -i filelist.txt: input file list
        # -vf scale: scale to specified resolution, maintaining aspect ratio
        # -c:v libx264: use H.264 codec
        # -pix_fmt yuv420p: pixel format for compatibility
        # -y: overwrite output file
        
        # Parse resolution
        width, height = resolution.split('x')
        
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(filelist_path),
            '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-y',
            str(output_path)
        ]
        
        print(f"\nRunning ffmpeg command...")
        print(f"Output will be saved to: {output_path}")
        
        # Run ffmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n✓ Video created successfully: {output_path}")
            file_size = output_path.stat().st_size / (1024 * 1024)  # Convert to MB
            print(f"  File size: {file_size:.2f} MB")
            return True
        else:
            print(f"\n✗ Error creating video:")
            print(result.stderr)
            return False
            
    finally:
        # Clean up temporary file list
        if filelist_path.exists():
            filelist_path.unlink()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create MP4 video from images in arabic-plates directory")
    parser.add_argument("--fps", type=int, default=2, help="Frames per second (default: 2)")
    parser.add_argument("--resolution", type=str, default="1280x720", help="Video resolution (default: 1280x720)")
    parser.add_argument("--output", type=str, default="arabic_plates_video.mp4", help="Output filename")
    
    args = parser.parse_args()
    
    success = create_video_from_images(
        fps=args.fps,
        resolution=args.resolution,
        output_file=args.output
    )
    
    exit(0 if success else 1)
