# Arabic OCR Test Script using PaddleOCR Arabic Model
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont
import os

# Initialize PaddleOCR with Arabic language support
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang='ar',  # Arabic language
    det_db_thresh=0.1,  # Very low threshold for text detection
    det_db_box_thresh=0.3,  # Very low threshold for box detection
    det_db_unclip_ratio=2.0,  # Increase unclip ratio for better detection
    drop_score=0.2)  # Very low confidence threshold

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# Use local image file
source_image = "arabic_plates/6.jpg"
image_path = source_image

print(f"Using local image: {image_path}")
print("Running Arabic OCR...")

# Run OCR inference
result = ocr.ocr(image_path, cls=False)

# Debug: Print raw result
print(f"\nDebug - Raw result: {result}")
print(f"Debug - Number of detections: {len(result[0]) if result and result[0] else 0}")

# Print the results
print("\n" + "="*60)
print("ARABIC OCR RESULTS")
print("="*60)

if result and result[0]:
    for idx, line in enumerate(result[0]):
        box = line[0]  # Bounding box coordinates
        text = line[1][0]  # Text
        confidence = line[1][1]  # Confidence score
        
        print(f"\nLine {idx + 1}:")
        print(f"  Text: '{text}'")
        print(f"  Confidence: {confidence:.4f}")
        print(f"  Box: {box}")
else:
    print("No text detected!")

# Visualize and save the result
print("\n" + "="*60)
print("Generating annotated image...")
image = Image.open(image_path).convert('RGB')

# Use PIL to draw boxes and text
draw = ImageDraw.Draw(image)

# Extract boxes and texts from result
if result and result[0]:
    for idx, line in enumerate(result[0]):
        box = line[0]  # Bounding box coordinates
        text = line[1][0]  # Text
        confidence = line[1][1]  # Confidence score
        
        # Convert box to polygon format for PIL
        polygon = [(int(point[0]), int(point[1])) for point in box]
        
        # Draw the bounding box
        draw.polygon(polygon, outline='red', width=3)
        
        # Draw text label (using default font)
        try:
            # Try to use a default font
            font = ImageFont.load_default()
            text_label = f"{text} ({confidence:.2f})"
            
            # Position text at top-left of box
            text_position = (int(box[0][0]), max(0, int(box[0][1]) - 20))
            
            # Draw text with background for better visibility
            bbox = draw.textbbox(text_position, text_label, font=font)
            draw.rectangle(bbox, fill='red')
            draw.text(text_position, text_label, fill='white', font=font)
        except Exception as e:
            # If font fails, just draw the box
            pass

# Save the annotated image
output_path = "output/arabic_ocr_result.png"
image.save(output_path)
print(f"Annotated image saved to {output_path}")
print(f"\nTotal text lines detected: {len(result[0]) if result and result[0] else 0}")
print("="*60)
