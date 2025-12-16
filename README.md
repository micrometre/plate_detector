# PaddleDetection UK Vehicle License Plate Recognition
### PP-Vehicle License Plate Recognition Modules

A comprehensive **UK license plate recognition system** using PaddleDetection's vehicle detection pipeline, adapted for **UK license plates** and based on the [official tutorial](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.8.1/deploy/pipeline/docs/tutorials/ppvehicle_plate_en.md).





## ✨ Features



```

- 🚗 Complete vehicle detection pipeline
- 🆔 UK license plate detection and recognition  
- 🇸🇦 Arabic license plate detection and recognition
- 📝 Real OCR using PaddleOCR for UK and Arabic license plates
- 🇬🇧 Support for UK license plate formats (AB12 CDE, M123 ABC, etc.)
- 🌍 Support for Arabic license plate formats with Arabic characters
- 🎨 Image visualization with detection results
- 📊 Batch processing of multiple images
- 🎬 **Video processing support** - Process video files frame-by-frame
- 🖥️ **CPU-only compatible** - No GPU required!
- ⚡ Optimized for CPU performance

## 🏭 Full PaddleOCR Version (🖥️ CPU Compatible)

This is a complete PaddleDetection integration for UK license plate recognition, **optimized for CPU-only systems**:

```
PaddleDetection UK Vehicle License Plate Recognition - Full Pipeline

```

## 🚀 Quick Start 

### 🖥️ Automated CPU Setup (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/micrometre/paddle_detection
cd paddle_detection

# 2. Run automated CPU setup
chmod +x setup.sh
./setup.sh

# 3. Activate environment and configure CPU
source .venv/bin/activate
source cpu_config.sh

```


### Usage

```bash

# Arabic license plate processing
python test_draw_results.py --config deploy/pipeline/config/infer_cfg_ppvehicle.yml --input-dir arabic_plates/ --output-dir output



python deploy/pipeline/pipeline.py \
    --config deploy/pipeline/config/infer_cfg_ppvehicle.yml \
    --image_file test_data/1.jpg \
    --output_dir output



# UK license plate video processing
python deploy/pipeline/pipeline.py \
  --config deploy/pipeline/config/infer_cfg_ppvehicle.yml \
  --video_file test_data/1.mp4 \
  --frame_skip 25 \
  --save_frames

# Arabic license plate video processing
python deploy/pipeline/pipeline.py \
  --config deploy/pipeline/config/infer_cfg_ppvehicle_arabic.yml \
  --video_file test_data/arabic_video.mp4 \
  --frame_skip 25 \
  --save_frames



```



### CPU Configuration
```bash
# Force CPU usage (disable GPU detection)
export CUDA_VISIBLE_DEVICES=""
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
```

## 📁 Project Structure

```
paddle_detection/
├── deploy/
│   └── pipeline/
│       ├── config/
│       │   └── infer_cfg_ppvehicle.yml   # Configuration file (UK settings)
│       ├── ppvehicle/
│       │   └── uk_license_dict.txt       # UK license plate dictionary
│       └── pipeline.py                   # Full PaddleOCR version
├── test_data/
│   ├── 1.jpg                            # Test image 1
│   └── 2.jpg                            # Test image 2
├── requirements.txt                     # CPU-only dependencies
├── setup.sh                           # Automated CPU setup script
├── run_demo.sh                        # CPU-optimized demo script
├── test_cpu.py                        # CPU compatibility test
├── test_video.py                      # Video processing test
├── cpu_config.sh                      # CPU configuration (generated)
└── README.md                          # This file
```

## ⚙️ Configuration

The system is configured through `deploy/pipeline/config/infer_cfg_ppvehicle.yml`:

```yaml
# UK License Plate Recognition Configuration
MODEL:
  vehicle_plate: True
  plate_text: True
  
OCR:
  lang: 'en'  # English for UK license plates
  rec_algorithm: 'SVTR_LCNet'
  
REID:
  model_dir: null
  
THRESHOLD:
  vehicle_plate: 0.5
  plate_text: 0.3
```

## 🎨 Customization

### UK License Plate Formats
The system supports various UK license plate formats:
- Current format: `AB12 CDE`
- Older format: `M123 ABC`
- European format: `AB-12-CDE`

### Arabic License Plate Formats
The system supports Arabic license plates with:
- Arabic numerals (0-9) and Arabic-Indic numerals (٠-٩)
- English letters (A-Z)
- Arabic alphabet (28 letters: ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي)
- Special characters used in various Arabic countries

### Adding New Formats
- For UK plates: Edit `deploy/pipeline/ppvehicle/uk_license_dict.txt`
- For Arabic plates: Edit `deploy/pipeline/ppvehicle/arabic_license_dict.txt`



## 📄 License

This project is based on PaddleDetection and follows the Apache 2.0 License.

## 🙏 Acknowledgments

- [PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection) for the vehicle detection pipeline
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) for optical character recognition
- UK DVLA for license plate format specifications

---

🇬🇧 **Made for UK License Plate Recognition** 🚗



python deploy/pipeline/pipeline.py --config  deploy/pipeline/config/infer_cfg_ppvehicle.yml --video_file test_data/1.mp4 --frame_skip 5 --save_frames
