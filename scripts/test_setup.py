#!/usr/bin/env python
"""
Test script to validate the PaddleDetection setup
"""
import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    try:
        import yaml
        print("✓ PyYAML imported successfully")
    except ImportError as e:
        print(f"✗ PyYAML import failed: {e}")
        return False
        
    try:
        import numpy as np
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
        
    try:
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
        
    try:
        import paddle
        print(f"✓ PaddlePaddle {paddle.__version__} imported successfully")
    except ImportError as e:
        print(f"✗ PaddlePaddle import failed: {e}")
        return False
        
    try:
        from paddleocr import PaddleOCR
        print("✓ PaddleOCR imported successfully")
    except ImportError as e:
        print(f"✗ PaddleOCR import failed: {e}")
        return False
        
    return True

def test_files():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "deploy/pipeline/pipeline.py",
        "deploy/pipeline/config/infer_cfg_ppvehicle.yml",
        "deploy/pipeline/ppvehicle/rec_word_dict.txt",
        "requirements.txt",
        "setup.sh",
        "README.md"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False
            
    return all_exist

def test_config():
    """Test if configuration file is valid"""
    print("\nTesting configuration file...")
    
    try:
        import yaml
        with open("deploy/pipeline/config/infer_cfg_ppvehicle.yml", 'r') as f:
            config = yaml.safe_load(f)
        
        if 'VEHICLE_PLATE' in config:
            print("✓ Configuration file is valid")
            print(f"  - VEHICLE_PLATE.enable: {config['VEHICLE_PLATE'].get('enable', 'not set')}")
            return True
        else:
            print("✗ Configuration file missing VEHICLE_PLATE section")
            return False
    except Exception as e:
        print(f"✗ Configuration file test failed: {e}")
        return False

def test_test_images():
    """Test if test images exist"""
    print("\nTesting test images...")
    
    test_dir = Path("test_data")
    if not test_dir.exists():
        print("✗ test_data directory missing")
        return False
        
    image_files = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.png"))
    if image_files:
        print(f"✓ Found {len(image_files)} test images:")
        for img in image_files:
            print(f"  - {img}")
        return True
    else:
        print("✗ No test images found in test_data/")
        return False

def main():
    print("PaddleDetection Vehicle License Plate Recognition - Setup Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Run tests
    if test_imports():
        tests_passed += 1
        
    if test_files():
        tests_passed += 1
        
    if test_config():
        tests_passed += 1
        
    if test_test_images():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Test Summary: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("\n🎉 All tests passed! The setup is ready to use.")
        print("\nNext steps:")
        print("1. Activate virtual environment: source .venv/bin/activate")
        print("2. Run detection: python deploy/pipeline/pipeline.py --config deploy/pipeline/config/infer_cfg_ppvehicle.yml --image_file test_data/1.jpg")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        print("Try running: ./setup.sh")
        
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
