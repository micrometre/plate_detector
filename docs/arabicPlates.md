Arabic Character Recognition Pipeline Setup
This plan outlines the steps to configure the license plate detection pipeline to recognize Arabic characters, enabling support for Arabic license plates alongside the existing UK license plate system.

Background
The current system is configured for UK license plates with:

English OCR models (lang='en')
UK character dictionary at 
deploy/pipeline/ppvehicle/uk_license_dict.txt
Configuration file: 
deploy/pipeline/config/infer_cfg_ppvehicle.yml
An Arabic character dictionary already exists at 
deploy/pipeline/ppvehicle/arabic_license_dict.txt
 containing:

Arabic numerals (0-9)
Arabic-Indic numerals (٠-٩)
English letters (A-Z)
Arabic alphabet (28 letters)
Special characters used in Arabic plates
User Review Required
IMPORTANT

Language Model Selection: PaddleOCR supports Arabic language with lang='ar' or lang='arabic'. The implementation will use the Arabic language model which may require downloading additional model files on first run.

IMPORTANT

Configuration Approach: This plan creates a separate Arabic configuration file (infer_cfg_ppvehicle_arabic.yml) to allow switching between UK and Arabic license plate recognition. Alternatively, we could modify the existing configuration or add a language parameter. Please confirm if you prefer a separate config file or a unified approach.

Proposed Changes
Configuration Files
[NEW] 
infer_cfg_ppvehicle_arabic.yml
Create a new configuration file specifically for Arabic license plate recognition:

Set ocr_language: "ar" (Arabic)
Point word_dict_path to 
deploy/pipeline/ppvehicle/arabic_license_dict.txt
Adjust detection thresholds optimized for Arabic script:
det_db_thresh: 0.3 (slightly higher for Arabic script complexity)
det_db_box_thresh: 0.5 (increased for better bounding box accuracy)
rec_thresh: 0.5 (higher recognition threshold for Arabic characters)
Configure Arabic OCR model paths
Pipeline Code
[MODIFY] 
pipeline.py
Update the VehiclePlateDetector.setup_models() method to:

Read the ocr_language setting from the configuration file
Initialize PaddleOCR with the appropriate language parameter
Support both English (lang='en') and Arabic (lang='ar') languages
Add proper error handling for Arabic model initialization
Ensure UTF-8 encoding for Arabic text output
The changes will maintain backward compatibility with the existing UK license plate configuration.

Documentation
[MODIFY] 
README.md
Update documentation to:

Add Arabic license plate recognition to the features list
Include usage example for Arabic configuration
Document the Arabic character dictionary
Add notes about Arabic model download on first run
Verification Plan
Automated Tests
Since there are no existing automated tests in the repository, verification will be done through manual testing.

Manual Verification
Test Arabic Configuration Loading

# Verify the Arabic configuration file is valid
python -c "import yaml; print(yaml.safe_load(open('deploy/pipeline/config/infer_cfg_ppvehicle_arabic.yml')))"
Test Arabic OCR Initialization

# Test that PaddleOCR can initialize with Arabic language
python -c "from paddleocr import PaddleOCR; ocr = PaddleOCR(lang='ar', use_gpu=False); print('Arabic OCR initialized successfully')"
Test Pipeline with Arabic Configuration

# Run the pipeline with Arabic configuration on a test image
# Note: User will need to provide a test image with Arabic license plates
python deploy/pipeline/pipeline.py \
  --config deploy/pipeline/config/infer_cfg_ppvehicle_arabic.yml \
  --image_file test_data/arabic_plate.jpg
Verify Arabic Character Recognition

User should provide sample images of Arabic license plates
Check that the output correctly recognizes Arabic characters
Verify that Arabic text is properly displayed in the output (UTF-8 encoding)
Confirm that detection boxes are drawn correctly around Arabic text
Test Backward Compatibility

# Ensure UK configuration still works
python deploy/pipeline/pipeline.py \
  --config deploy/pipeline/config/infer_cfg_ppvehicle.yml \
  --image_file test_data/1.jpg
NOTE

The user will need to provide test images containing Arabic license plates for proper verification. If test images are not available, we can proceed with the implementation and test with the UK configuration to ensure no regressions.