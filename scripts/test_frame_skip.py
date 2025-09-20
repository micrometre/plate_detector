#!/usr/bin/env python3
"""
Test frame skipping functionality with different skip values
"""
import os
import time
import subprocess

def test_frame_skip():
    """Test different frame skip values"""
    print("🎬 Testing Frame Skip Functionality")
    print("=" * 50)
    
    # Ensure test video exists
    if not os.path.exists("test_data/test_video.mp4"):
        print("❌ Test video not found. Creating it first...")
        os.system("python3 test_video.py > /dev/null 2>&1")
    
    # Test different skip values
    skip_values = [1, 2, 3, 5]
    results = []
    
    for skip in skip_values:
        print(f"\n🔄 Testing frame_skip = {skip}")
        print("-" * 30)
        
        output_dir = f"output_skip_{skip}"
        
        # Build command
        cmd = (
            f"/bin/bash -c 'source .venv/bin/activate && source cpu_config.sh && "
            f"python deploy/pipeline/pipeline.py "
            f"--config deploy/pipeline/config/infer_cfg_ppvehicle.yml "
            f"--video_file test_data/test_video.mp4 "
            f"--output_dir {output_dir} "
            f"--save_video --save_frames "
            f"--frame_skip {skip}'"
        )
        
        # Time the processing
        start_time = time.time()
        print(f"📝 Running: frame_skip={skip}")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Check results
        if result.returncode == 0:
            # Count processed frames
            annotated_dir = f"{output_dir}/frames_test_video/annotated"
            if os.path.exists(annotated_dir):
                frame_count = len([f for f in os.listdir(annotated_dir) if f.endswith('.jpg')])
            else:
                frame_count = 0
            
            results.append({
                'skip': skip,
                'time': processing_time,
                'frames': frame_count,
                'success': True
            })
            
            print(f"✅ Success: {frame_count} frames processed in {processing_time:.1f}s")
            
            # Check video size
            video_path = f"{output_dir}/result_test_video.mp4"
            if os.path.exists(video_path):
                video_size = os.path.getsize(video_path) / (1024*1024)
                print(f"📊 Output video size: {video_size:.1f} MB")
        else:
            results.append({
                'skip': skip,
                'time': processing_time,
                'frames': 0,
                'success': False
            })
            print(f"❌ Failed after {processing_time:.1f}s")
            if result.stderr:
                print(f"Error: {result.stderr[:100]}...")
    
    # Print summary
    print(f"\n{'='*70}")
    print("🎯 FRAME SKIP PERFORMANCE SUMMARY")
    print(f"{'='*70}")
    print(f"{'Skip':<6} {'Frames':<8} {'Time (s)':<10} {'Speed Up':<10} {'Status'}")
    print("-" * 50)
    
    baseline_time = None
    for r in results:
        if r['success'] and r['skip'] == 1:
            baseline_time = r['time']
            break
    
    for r in results:
        if r['success']:
            speed_up = f"{baseline_time/r['time']:.1f}x" if baseline_time else "N/A"
            status = "✅ OK"
        else:
            speed_up = "N/A"
            status = "❌ FAIL"
        
        print(f"{r['skip']:<6} {r['frames']:<8} {r['time']:<10.1f} {speed_up:<10} {status}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if baseline_time:
        print(f"   • frame_skip=1: Full processing (baseline)")
        print(f"   • frame_skip=2: 2x faster, half the frames")
        print(f"   • frame_skip=3: 3x faster, every 3rd frame")
        print(f"   • frame_skip=5: 5x faster, every 5th frame")
        print(f"   • Higher skip values trade accuracy for speed")

if __name__ == "__main__":
    test_frame_skip()
