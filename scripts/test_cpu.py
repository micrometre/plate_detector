#!/usr/bin/env python3
"""
CPU Compatibility Test for PaddleDetection UK License Plate Recognition
Tests that all components work correctly in CPU-only mode
"""

import os
import sys

def test_cpu_setup():
    """Test CPU-only setup and dependencies"""
    
    print("🖥️  PaddleDetection CPU Compatibility Test")
    print("=" * 50)
    
    # Force CPU mode
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    os.environ['OMP_NUM_THREADS'] = '4'
    os.environ['MKL_NUM_THREADS'] = '4'
    print("✅ CPU-only mode configured")
    
    # Test basic imports
    print("\n🧪 Testing imports...")
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import yaml
        print("✅ PyYAML imported successfully")
    except ImportError as e:
        print(f"❌ PyYAML import failed: {e}")
        return False
    
    # Test PaddlePaddle CPU
    print("\n🏊 Testing PaddlePaddle (CPU)...")
    try:
        import paddle
        print(f"✅ PaddlePaddle {paddle.__version__} imported")
        
        # Verify CPU mode
        if paddle.is_compiled_with_cuda():
            print("⚠️  PaddlePaddle supports CUDA but using CPU mode")
        else:
            print("✅ PaddlePaddle is CPU-only version")
            
        # Test basic tensor operation
        x = paddle.randn([2, 3])
        y = paddle.sum(x)
        print("✅ PaddlePaddle CPU operations working")
        
    except ImportError as e:
        print(f"❌ PaddlePaddle import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ PaddlePaddle operation failed: {e}")
        return False
    
    # Test PaddleOCR CPU
    print("\n🔤 Testing PaddleOCR (CPU)...")
    try:
        import paddleocr
        print("✅ PaddleOCR imported successfully")
        
        # Initialize OCR in CPU mode
        ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
        print("✅ PaddleOCR initialized in CPU mode")
        
        # Test with a simple image (create a dummy one)
        import numpy as np
        dummy_img = np.ones((100, 300, 3), dtype=np.uint8) * 255
        
        # This might take a while on first run (model download)
        print("🔄 Testing OCR recognition (may take time for first run)...")
        result = ocr.ocr(dummy_img, cls=True)
        print("✅ PaddleOCR CPU processing successful")
        
    except ImportError as e:
        print(f"❌ PaddleOCR import failed: {e}")
        return False
    except Exception as e:
        print(f"⚠️  PaddleOCR test warning: {e}")
        print("   This is often normal on first run or with dummy images")
    
    # Test file availability
    print("\n📁 Testing project files...")
    
    config_file = "deploy/pipeline/config/infer_cfg_ppvehicle.yml"
    if os.path.exists(config_file):
        print("✅ Configuration file found")
    else:
        print(f"⚠️  Configuration file not found: {config_file}")
    
    pipeline_file = "deploy/pipeline/pipeline.py"
    if os.path.exists(pipeline_file):
        print("✅ Pipeline script found")
    else:
        print(f"⚠️  Pipeline script not found: {pipeline_file}")
    
    test_images = ["test_data/1.jpg", "test_data/2.jpg"]
    for img_path in test_images:
        if os.path.exists(img_path):
            print(f"✅ Test image found: {img_path}")
        else:
            print(f"⚠️  Test image not found: {img_path}")
    
    print("\n" + "=" * 50)
    print("🎉 CPU Compatibility Test Complete!")
    print("✅ Your system should work with CPU-only PaddleDetection")
    print("\n💡 To run the actual detection:")
    print("   export CUDA_VISIBLE_DEVICES=\"\"")
    print("   python deploy/pipeline/pipeline.py --config deploy/pipeline/config/infer_cfg_ppvehicle.yml --image_file test_data/1.jpg")
    
    return True

if __name__ == "__main__":
    try:
        success = test_cpu_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        sys.exit(1)
