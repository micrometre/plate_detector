#!/usr/bin/env python3
"""
Simple test API server to receive license plate detection results
Run this server to test the HTTP functionality of the pipeline.

Usage:
    python test_api_server.py
    
Then run the pipeline with --send_to_api flag:
    python deploy/pipeline/pipeline.py --config config.yml --video_file video.mp4 --send_to_api
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import datetime

class LicensePlateHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests with detection results"""
        try:
            # Get content length
            content_length = int(self.headers['Content-Length'])
            
            # Read the POST data
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            
            # Print received data
            print(f"\n{'='*60}")
            print(f"📡 RECEIVED DETECTION RESULTS")
            print(f"{'='*60}")
            print(f"🕒 Timestamp: {data.get('timestamp', 'N/A')}")
            print(f"🎬 Video file: {data.get('video_file', 'N/A')}")
            print(f"📊 Total detections: {data.get('total_detections', 0)}")
            print(f"{'='*60}")
            
            # Process detections
            detections = data.get('detections', [])
            for i, detection in enumerate(detections, 1):
                print(f"🚗 Detection #{i}:")
                print(f"   License Plate: {detection.get('license_plate', 'N/A')}")
                print(f"   Confidence: {detection.get('confidence', 0):.3f}")
                print(f"   Frame: {detection.get('frame_number', 'N/A')}")
                print(f"   UUID: {detection.get('uuid', 'N/A')}")
                print(f"   Frame Filename: {detection.get('frame_filename', 'N/A')}")
                if detection.get('original_frame_path'):
                    print(f"   Original Frame Path: {detection.get('original_frame_path')}")
                if detection.get('annotated_frame_path'):
                    print(f"   Annotated Frame Path: {detection.get('annotated_frame_path')}")
                print()
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "success",
                "message": f"Received {len(detections)} detections",
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Error processing request: {e}")
            
            # Send error response
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error_response = {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_GET(self):
        """Handle GET requests - simple status check"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "running",
            "message": "License Plate API Server is running",
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Custom log message to reduce noise"""
        print(f"🌐 {self.address_string()} - {format % args}")

def run_server(port=8000):
    """Run the test API server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, LicensePlateHandler)
    
    print(f"🚀 License Plate API Server starting on port {port}")
    print(f"📡 Listening for POST requests at http://localhost:{port}")
    print(f"🔍 Status check available at http://localhost:{port}")
    print(f"⏹️  Press Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
