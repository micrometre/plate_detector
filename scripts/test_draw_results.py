#!/usr/bin/env python3
"""
Test script to demonstrate the draw_results function.
This processes a single image and draws the detection results on it.
"""
import os
import sys

# Add the deploy/pipeline directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'deploy', 'pipeline'))

from pipeline import VehiclePlateDetector
import cv2

def test_draw_results(config_path, image_path, output_path):
    """
    Test the draw_results method by processing a single image.
    
    Args:
        config_path: Path to the configuration YAML file
        image_path: Path to the input image
        output_path: Path where the annotated image will be saved
    """
    print(f"Initializing detector with config: {config_path}")
    detector = VehiclePlateDetector(config_path)
    
    print(f"Reading image: {image_path}")
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Could not read image from {image_path}")
        return False
    
    print("Processing image to detect license plates...")
    results = detector.process_frame(image)
    
    if not results:
        print("No license plates detected in the image")
        return False
    
    print(f"Found {len(results)} license plate(s):")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['license_plate']} (confidence: {result['confidence']:.2f})")
    
    print(f"\nDrawing results on image...")
    success = detector.draw_results(image_path, results, output_path)
    
    if success:
        print(f"✓ Annotated image saved to: {output_path}")
        return True
    else:
        print("✗ Failed to draw results")
        return False

def process_directory(config_path, input_dir, output_dir):
    """
    Process all images in a directory and save annotated results.
    
    Args:
        config_path: Path to the configuration YAML file
        input_dir: Directory containing input images
        output_dir: Directory where annotated images will be saved
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    
    # Get all image files from the input directory
    image_files = [
        f for f in os.listdir(input_dir)
        if os.path.splitext(f.lower())[1] in image_extensions
    ]
    
    if not image_files:
        print(f"No image files found in {input_dir}")
        return False
    
    print(f"Found {len(image_files)} image(s) to process")
    print(f"Initializing detector with config: {config_path}")
    detector = VehiclePlateDetector(config_path)
    
    success_count = 0
    failed_count = 0
    
    for idx, image_file in enumerate(image_files, 1):
        input_path = os.path.join(input_dir, image_file)
        output_path = os.path.join(output_dir, f"annotated_{image_file}")
        
        print(f"\n[{idx}/{len(image_files)}] Processing: {image_file}")
        
        # Read image
        image = cv2.imread(input_path)
        if image is None:
            print(f"  ✗ Error: Could not read image")
            failed_count += 1
            continue
        
        # Process image
        results = detector.process_frame(image)
        
        if not results:
            print(f"  ⚠ No license plates detected")
            # Still save the image without annotations
            cv2.imwrite(output_path, image)
            success_count += 1
            continue
        
        print(f"  Found {len(results)} license plate(s):")
        for i, result in enumerate(results, 1):
            print(f"    {i}. {result['license_plate']} (confidence: {result['confidence']:.2f})")
        
        # Draw results
        if detector.draw_results(input_path, results, output_path):
            print(f"  ✓ Saved to: {output_path}")
            success_count += 1
        else:
            print(f"  ✗ Failed to draw results")
            failed_count += 1
    
    print(f"\n{'='*60}")
    print(f"Processing complete: {success_count} succeeded, {failed_count} failed")
    print(f"Output directory: {output_dir}")
    
    return failed_count == 0

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the draw_results function")
    parser.add_argument("--config", type=str, required=True,
                        help="Path to config file (e.g., deploy/pipeline/config/infer_cfg_ppvehicle.yml)")
    parser.add_argument("--image", type=str,
                        help="Path to input image (use either --image or --input-dir)")
    parser.add_argument("--input-dir", type=str,
                        help="Directory containing input images to process (use either --image or --input-dir)")
    parser.add_argument("--output", type=str, default="output_annotated.jpg",
                        help="Path to output annotated image (used with --image, default: output_annotated.jpg)")
    parser.add_argument("--output-dir", type=str, default="output_annotated",
                        help="Directory for output annotated images (used with --input-dir, default: output_annotated)")
    
    args = parser.parse_args()
    
    # Validate that either --image or --input-dir is provided, but not both
    if args.image and args.input_dir:
        print("Error: Please specify either --image or --input-dir, not both")
        sys.exit(1)
    
    if not args.image and not args.input_dir:
        print("Error: Please specify either --image or --input-dir")
        sys.exit(1)
    
    # Validate config file
    if not os.path.exists(args.config):
        print(f"Error: Config file not found: {args.config}")
        sys.exit(1)
    
    # Process based on mode
    if args.image:
        # Single image mode
        if not os.path.exists(args.image):
            print(f"Error: Image file not found: {args.image}")
            sys.exit(1)
        
        success = test_draw_results(args.config, args.image, args.output)
    else:
        # Directory mode
        if not os.path.exists(args.input_dir):
            print(f"Error: Input directory not found: {args.input_dir}")
            sys.exit(1)
        
        if not os.path.isdir(args.input_dir):
            print(f"Error: {args.input_dir} is not a directory")
            sys.exit(1)
        
        success = process_directory(args.config, args.input_dir, args.output_dir)
    
    sys.exit(0 if success else 1)
