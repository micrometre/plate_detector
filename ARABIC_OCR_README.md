# Arabic License Plate OCR - Summary

## Overview
Successfully created Arabic OCR scripts for license plate detection using PaddleOCR with Arabic language support.

## Files Created

### 1. `paddle_test.py`
- Basic PaddleOCR test script
- Supports both English and Arabic OCR
- Processes single images
- Saves annotated output images

### 2. `paddle_arabic_test.py`
- Dedicated Arabic OCR test script
- Enhanced output formatting
- Debug information display
- Fixed image path (arabic_plates/6.jpg)

### 3. `arabic_ocr.py` ⭐ **RECOMMENDED**
- **Most comprehensive solution**
- Command-line interface
- Supports single image or directory processing
- Better error handling and output formatting
- Numbered annotations on output images

## Usage

### Process a single image:
```bash
python arabic_ocr.py arabic_plates/6.jpg
```

### Process entire directory:
```bash
python arabic_ocr.py arabic_plates/
```

### Use default image (if no argument provided):
```bash
python arabic_ocr.py
```

## Configuration

The Arabic OCR model is configured with optimized parameters for license plate detection:

```python
ocr = PaddleOCR(
    lang='ar',                    # Arabic language
    det_db_thresh=0.1,           # Low threshold for text detection
    det_db_box_thresh=0.3,       # Low threshold for box detection
    det_db_unclip_ratio=2.0,     # Increase unclip ratio for better detection
    drop_score=0.2               # Low confidence threshold
)
```

## Results

The script successfully detects Arabic text in license plates:
- Arabic numerals (e.g., '٢٢', '٣٣٨٧')
- Arabic text (e.g., 'ةيدوعسلا' - "Saudi")
- Mixed Arabic/Latin characters
- Numbers in Western format

### Example Output (image 6.jpg):
- Region 1: '٢٢' (confidence: 0.7791)
- Region 2: 'ىحر' (confidence: 0.8327)
- Region 3: 'ةيدوعسلا' (confidence: 0.8809)
- Region 4: '020' (confidence: 0.5307)
- Region 5: 'لR' (confidence: 0.7646)

## Output Files

All annotated images are saved to the `output/` directory with the naming pattern:
- `{original_filename}_arabic_ocr.png`

Each output image shows:
- Red bounding boxes around detected text
- Numbered labels with detected text and confidence scores

## Model Information

- **Detection Model**: Multilingual_PP-OCRv3_det_infer
- **Recognition Model**: arabic_PP-OCRv4_rec_infer
- **Dictionary**: arabic_dict.txt
- **Source**: PaddlePaddle/PaddleOCR

## References

- PaddleOCR GitHub: https://github.com/PaddlePaddle/PaddleOCR
- Arabic Model: https://huggingface.co/PaddlePaddle/arabic_PP-OCRv3_mobile_rec
- Documentation: https://paddlepaddle.github.io/PaddleOCR/

## Next Steps

For better license plate recognition, consider:
1. Fine-tuning the model on your specific license plate dataset
2. Using a specialized license plate OCR model
3. Pre-processing images (contrast enhancement, noise reduction)
4. Post-processing to validate license plate formats
