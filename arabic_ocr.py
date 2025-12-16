#!/usr/bin/env python3
"""
Arabic License Plate OCR Script
Uses PaddleOCR with Arabic language support to detect and recognize text in license plate images.
"""

from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont
import os
import sys
import glob

def process_image(ocr, image_path, output_dir="output"):
    """
    Process a single image with Arabic OCR
    
    Args:
        ocr: PaddleOCR instance
        image_path: Path to the input image
        output_dir: Directory to save output files
    
    Returns:
        List of detected text results
    """
    print(f"\n{'='*60}")
    print(f"Processing: {image_path}")
    print(f"{'='*60}")
    
    # Run OCR inference
    result = ocr.ocr(image_path, cls=False)
    
    # Print the results
    if result and result[0]:
        print(f"\nDetected {len(result[0])} text regions:\n")
        
        for idx, line in enumerate(result[0]):
            box = line[0]  # Bounding box coordinates
            text = line[1][0]  # Text
            confidence = line[1][1]  # Confidence score
            
            print(f"Region {idx + 1}:")
            print(f"  Text: '{text}'")
            print(f"  Confidence: {confidence:.4f}")
            print(f"  Box: {box}")
            print()
    else:
        print("No text detected!")
        return []
    
    # Visualize and save the result
    print("Generating annotated image...")
    image = Image.open(image_path).convert('RGB')
    draw = ImageDraw.Draw(image)
    
    # Draw boxes and text
    if result and result[0]:
        for idx, line in enumerate(result[0]):
            box = line[0]
            text = line[1][0]
            confidence = line[1][1]
            
            # Convert box to polygon format for PIL
            polygon = [(int(point[0]), int(point[1])) for point in box]
            
            # Draw the bounding box
            draw.polygon(polygon, outline='red', width=3)
            
            # Draw text label
            try:
                font = ImageFont.load_default()
                text_label = f"{idx+1}: {text} ({confidence:.2f})"
                
                # Position text at top-left of box
                text_position = (int(box[0][0]), max(0, int(box[0][1]) - 20))
                
                # Draw text with background
                bbox = draw.textbbox(text_position, text_label, font=font)
                draw.rectangle(bbox, fill='red')
                draw.text(text_position, text_label, fill='white', font=font)
            except Exception as e:
                pass
    
    # Save the annotated image
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}_arabic_ocr.png")
    image.save(output_path)
    print(f"Annotated image saved to: {output_path}")
    
    return result[0] if result and result[0] else []


def main():
    """Main function"""
    # Initialize PaddleOCR with Arabic language support
    print("Initializing Arabic OCR model...")
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        lang='ar',  # Arabic language
        det_db_thresh=0.1,  # Low threshold for text detection
        det_db_box_thresh=0.3,  # Low threshold for box detection
        det_db_unclip_ratio=2.0,  # Increase unclip ratio
        drop_score=0.2)  # Low confidence threshold
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get image path from command line or use default
    if len(sys.argv) > 1:
        image_input = sys.argv[1]
    else:
        image_input = "arabic_plates/6.jpg"
    
    # Check if input is a directory or file
    if os.path.isdir(image_input):
        # Process all images in directory
        image_patterns = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
        image_files = []
        for pattern in image_patterns:
            image_files.extend(glob.glob(os.path.join(image_input, pattern)))
        
        if not image_files:
            print(f"No images found in directory: {image_input}")
            return
        
        print(f"Found {len(image_files)} images to process")
        
        for image_path in sorted(image_files):
            process_image(ocr, image_path, output_dir)
    
    elif os.path.isfile(image_input):
        # Process single image
        process_image(ocr, image_input, output_dir)
    
    else:
        print(f"Error: '{image_input}' is not a valid file or directory")
        return
    
    print(f"\n{'='*60}")
    print("Processing complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
