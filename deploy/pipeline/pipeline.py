#!/usr/bin/env python
"""
PaddleDetection UK Vehicle License Plate Recognition Video Pipeline
Based on PaddleDetection/deploy/pipeline/pipeline.py

Features:
- UK license plate detection and recognition
- Video file processing (MP4, AVI, WebM, MOV, MKV, etc.)
- CPU-optimized processing
- Comprehensive detection summaries
- HTTP API integration for sending results with frame paths
- WebM file support for camera streaming

Usage:
  # Basic video processing (supports WebM files)
  python pipeline.py --config config.yml --video_file video.webm
  
  # Send results to API (includes frame paths if --save_frames is used)
  python pipeline.py --config config.yml --video_file video.webm --send_to_api --save_frames
  
  # Custom API endpoint
  python pipeline.py --config config.yml --video_file video.webm --send_to_api --api_endpoint http://localhost:9000
"""
import os
import sys
import argparse
import cv2
import yaml
import requests
import uuid
import time

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import paddle
    print(f"PaddlePaddle version: {paddle.__version__}")
except ImportError:
    print("PaddlePaddle not installed. Installing...")
    import paddle

try:
    from paddleocr import PaddleOCR
    print("PaddleOCR is available")
except ImportError:
    print("PaddleOCR not installed. Installing...")
    from paddleocr import PaddleOCR

class VehiclePlateDetector:
    def __init__(self, config_path):
        """Initialize the vehicle plate detector"""
        self.config = self.load_config(config_path)
        self.setup_models()
        
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
        
    def setup_models(self):
        """Setup OCR models for UK license plate detection and recognition"""
        try:
            # Check OpenCV version and codec support
            print(f"OpenCV version: {cv2.__version__}")
            
            # Initialize PaddleOCR for UK license plate detection and recognition
            # Use English language for UK plates
            self.ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
            print("PaddleOCR initialized successfully for UK license plates")
        except Exception as e:
            print(f"Error initializing PaddleOCR: {e}")
            # Simple fallback
            self.ocr = PaddleOCR(lang='en')
            print("PaddleOCR initialized with fallback settings for UK plates")
        
    def detect_vehicles(self, image):
        """Mock vehicle detection - in real implementation, use PP-YOLOE"""
        # For this minimal example, we'll assume the entire image contains a vehicle
        h, w = image.shape[:2]
        # Return a bounding box covering most of the image
        return [(int(w*0.1), int(h*0.1), int(w*0.9), int(h*0.9))]
        
    def detect_license_plates(self, image, vehicle_boxes):
        """Detect and recognize license plates in vehicle regions"""
        results = []
        
        for i, (x1, y1, x2, y2) in enumerate(vehicle_boxes):
            # Crop vehicle region
            vehicle_crop = image[y1:y2, x1:x2]
            
            # Use PaddleOCR to detect and recognize text (license plates)
            ocr_results = self.ocr.ocr(vehicle_crop, cls=True)
            
            if ocr_results and ocr_results[0]:
                for line in ocr_results[0]:
                    if line:
                        # Extract text and confidence
                        text = line[1][0]
                        confidence = line[1][1]
                        bbox = line[0]
                        
                        # Convert relative coordinates to absolute
                        abs_bbox = []
                        for point in bbox:
                            abs_x = int(point[0] + x1)
                            abs_y = int(point[1] + y1)
                            abs_bbox.append([abs_x, abs_y])
                        
                        results.append({
                            'license_plate': text.strip().upper().replace("I", "1"),
                            'confidence': confidence,
                            'bbox': abs_bbox,
                            'vehicle_bbox': [x1, y1, x2, y2]
                        })
                        
        return results
        
    def process_frame(self, frame):
        """Process a single video frame"""
        # Step 1: Detect vehicles
        vehicle_boxes = self.detect_vehicles(frame)
        
        # Step 2: Detect license plates
        plate_results = self.detect_license_plates(frame, vehicle_boxes)
        
        return plate_results
        
    def process_video(self, video_path, frames_dir=None, show_progress=True, frame_skip=1):
        """Process a video file frame by frame with optional frame skipping
        
        Args:
            video_path: Path to input video (supports mp4, avi, mov, webm, etc.)
            frames_dir: Directory to save individual frames (optional)
            show_progress: Show progress updates (default: True)
            frame_skip: Process every nth frame (default: 1 = every frame, 2 = every 2nd frame, etc.)
        """
        # Start timing
        start_time = time.time()
        
        # Check if video file exists
        if not os.path.exists(video_path):
            print(f"Error: Video file not found: {video_path}")
            return []
            
        # Get file extension to handle different video formats
        file_ext = os.path.splitext(video_path)[1].lower()
        supported_formats = ['.mp4', '.avi', '.mov', '.webm', '.mkv', '.flv', '.wmv']
        
        if file_ext not in supported_formats:
            print(f"Warning: Video format {file_ext} may not be fully supported. Supported formats: {supported_formats}")
        
        # Special handling for WebM files
        if file_ext == '.webm':
            print(f"Processing WebM file: {video_path}")
            # WebM files are supported by OpenCV, but we might need specific codec handling
            
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            # Try with different backend for WebM files
            if file_ext == '.webm':
                print("Trying alternative backend for WebM...")
                cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
                if not cap.isOpened():
                    print("Failed to open WebM file with FFMPEG backend")
                    return []
            else:
                return []
            
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Calculate effective processing stats
        frames_to_process = total_frames // frame_skip
        
        print(f"Video info: {fps} FPS, {total_frames} frames")
        if frame_skip > 1:
            print(f"Frame skip: Processing every {frame_skip} frame(s) ({frames_to_process} frames total)")
        
        # Create frames directory if needed (only for original frames)
        original_frames_dir = None
        if frames_dir:
            original_frames_dir = os.path.join(frames_dir)
            os.makedirs(original_frames_dir, exist_ok=True)
            print(f"Original frames will be saved to: {original_frames_dir}/")
        
        frame_count = 0
        processed_count = 0
        all_detections = []
        frames_with_detections = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            # Skip frames based on frame_skip parameter
            if (frame_count - 1) % frame_skip != 0:
                # If we're saving frames, we need to handle skipped frames
                if frames_dir:
                    # For skipped frames, we can either:
                    # 1. Copy the last processed frame's results
                    # 2. Save the frame without processing
                    # 3. Skip saving entirely
                    # For now, let's skip saving skipped frames to maintain processing efficiency
                    pass
                continue
                
            processed_count += 1
            
            if show_progress and processed_count % max(1, (frames_to_process // 10)) == 0:
                progress = (processed_count / frames_to_process) * 100
                print(f"Processing frame {frame_count}/{total_frames} (processed: {processed_count}/{frames_to_process}, {progress:.1f}%)")
            
            # Process frame
            results = self.process_frame(frame)
            
            # Generate UUID for this frame - this will be shared between detection payload and frame filename
            frame_uuid = str(uuid.uuid4())
            
            # Save individual frames if requested and prepare frame paths
            frame_filename = f"{frame_uuid}.jpg"
            original_frame_path = None
            
            if frames_dir:
                # Prepare frame path (only original)
                original_frame_path = os.path.join(original_frames_dir, frame_filename)
            
            # Store results with frame number and paths
            if results:
                frames_with_detections += 1
                for result in results:
                    result['frame'] = frame_count
                    result['frame_uuid'] = frame_uuid  # Add UUID to each result
                    result['original_frame_path'] = original_frame_path
                    result['frame_filename'] = frame_filename
                    all_detections.append(result)
            
            # Save individual frames if requested (only original frames)
            if frames_dir:
                cv2.imwrite(original_frame_path, frame)
            
        # Cleanup
        cap.release()
        
        # Calculate total processing time
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"Video processing complete!")
        print(f"Processed {frame_count} frames")
        print(f"Total processing time: {total_time:.2f} seconds")
        print(f"Average FPS: {frame_count / total_time:.2f} frames/second")
        print(f"Frames with detections: {frames_with_detections}")
        print(f"Total license plate detections: {len(all_detections)}")
        
        if frames_dir:
            print("Original frames saved")
        
        return all_detections

def send_results_to_api(results, endpoint_url="http://localhost:8000"):
    """Send detection results to API endpoint as JSON"""
    try:
        # Filter out results with empty license plates
        valid_results = [r for r in results if r.get('license_plate', '').strip()]
        
        if not valid_results:
            print("⚠️ No valid license plate detections to send to API")
            return True
        
        print(f"📤 Sending {len(valid_results)} valid detections to API...")
        
        # Send each detection individually as the Go backend expects
        success_count = 0
        
        for result in valid_results:
            # Ensure we have a valid license plate
            license_plate = result.get('license_plate', '').strip()
            if not license_plate:
                continue
                
            # Use the UUID from frame processing, or generate new one if missing
            detection_uuid = result.get('frame_uuid', str(uuid.uuid4()))
                
            # Prepare individual payload for each detection
            detection_payload = {
                "uuid": detection_uuid,
                "results": [
                    {
                        "plate": license_plate
                    }
                ]
            }
            
            # Send individual POST request for each detection
            headers = {'Content-Type': 'application/json'}
            response = requests.post(endpoint_url, json=detection_payload, headers=headers, timeout=30)
            
            if response.status_code in [200, 201]:
                success_count += 1
                print(f"✅ Successfully sent detection: {license_plate} (UUID: {detection_uuid})")
            else:
                print(f"❌ Failed to send detection {license_plate} (UUID: {detection_uuid}). Status: {response.status_code}, Response: {response.text}")
        
        if success_count == len(valid_results):
            print(f"✅ All {success_count} detections sent successfully to {endpoint_url}")
            return True
        else:
            print(f"⚠️ Sent {success_count}/{len(valid_results)} detections to {endpoint_url}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending data to API: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def parse_args():
    parser = argparse.ArgumentParser(description='PP-Vehicle License Plate Recognition Video Pipeline')
    parser.add_argument('--config', type=str, required=True,
                        help='Path to config file')
    parser.add_argument('--video_file', type=str, required=True,
                        help='Path to video file')
    parser.add_argument('--output_dir', type=str, default='output',
                        help='Output directory for results')
    parser.add_argument('--save_frames', action='store_true',
                        help='Save individual original frames as images')
    parser.add_argument('--frame_skip', type=int, default=1,
                        help='Process every nth frame (default: 1 = every frame, 2 = every 2nd frame, etc.)')
    parser.add_argument('--api_endpoint', type=str, default='http://localhost:8080/alprd',
                        help='API endpoint to send results to')
    parser.add_argument('--send_to_api', action='store_true',
                        help='Send detection results to API endpoint')
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Start total timing
    total_start_time = time.time()
    
    # Validate input video file
    if not os.path.exists(args.video_file):
        print(f"❌ Error: Video file not found: {args.video_file}")
        sys.exit(1)
    
    # Get video file information
    video_name = os.path.splitext(os.path.basename(args.video_file))[0]
    video_ext = os.path.splitext(args.video_file)[1].lower()
    
    print(f"📁 Input video: {args.video_file}")
    print(f"📁 Video format: {video_ext}")
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize detector
    detector = VehiclePlateDetector(args.config)
    
    # Process video
    print(f"🎬 Processing video: {args.video_file}")
    
    frames_dir = None
    if args.save_frames:
        frames_dir = os.path.join(args.output_dir)
    
    # Process video
    video_results = detector.process_video(args.video_file, frames_dir, frame_skip=args.frame_skip)
    
    # Calculate total execution time
    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time
    
    if not video_results:
        print("⚠️ No detection results obtained from video processing")
        return
    
    # Print summary
    print("\n" + "="*70)
    print("🎯 VIDEO PROCESSING SUMMARY")
    print("="*70)
    print(f"⏱️  Total execution time: {total_execution_time:.2f} seconds")
    print(f"📊 Total license plate detections: {len(video_results)}")
    
    # Group by unique license plates
    unique_plates = {}
    for result in video_results:
        plate = result['license_plate']
        if plate not in unique_plates:
            unique_plates[plate] = []
        unique_plates[plate].append(result)
    
    print(f"📊 Unique license plates detected: {len(unique_plates)}")
    
    # Send results to API if requested
    if args.send_to_api:
        print(f"\n🌐 Sending results to API endpoint: {args.api_endpoint}")
        success = send_results_to_api(video_results, args.api_endpoint)
        if success:
            print("✅ Results successfully sent to API")
        else:
            print("❌ Failed to send results to API")
    
    # Show unique plates with frame ranges
    for plate, detections in unique_plates.items():
        frames = [d['frame'] for d in detections]
        avg_conf = sum(d['confidence'] for d in detections) / len(detections)
        print(f"🚗 {plate}: frames {min(frames)}-{max(frames)} (avg conf: {avg_conf:.3f})")
    
    if args.save_frames:
        print(f"🖼️  Individual frames saved to: {frames_dir}/")
    
    if args.send_to_api:
        print(f"🌐 API endpoint: {args.api_endpoint}")
    
    print("="*70)

if __name__ == '__main__':
    main()