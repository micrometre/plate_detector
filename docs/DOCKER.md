# Docker Setup for PaddleDetection UK License Plate Recognition

This document provides instructions for running the UK License Plate Recognition system using Docker and Docker Compose.

## 🐳 Prerequisites

- Docker (version 20.10 or later)
- Docker Compose (version 2.0 or later)

## 🚀 Quick Start

### 1. Build the Docker Image

```bash
# Build the image using Makefile
make build

# Or build without cache (for development)
make dev-build

# Or use Docker Compose directly
docker-compose build
```

### 2. Run License Plate Detection

#### Pre-download Models (Recommended)

```bash
# Pre-download PaddleOCR models to avoid downloading every time
make download-models
```

#### Video Processing

```bash
# Process a video file
make video VIDEO=my_video.mp4

# Or using default video
make video

# Or using docker-compose directly
docker compose run --rm plate-detector
```

### 3. Interactive Shell

```bash
# Start an interactive bash shell inside the container
make shell

# Or development shell with source code mounted
make dev-shell

# Or using docker-compose directly
docker compose run --rm plate-detector bash
```

## 📁 Directory Structure

```
plate_detector/
├── Dockerfile              # Docker image definition
├── docker compose.yml      # Docker Compose configuration
├── Makefile                # Build and run tasks
├── .dockerignore           # Files to exclude from Docker build
├── test_data/              # Input images (mounted as /app/input)
├── output/                 # Detection results (mounted as /app/output)
├── videos/                 # Video files (mounted as /app/videos)
└── ...
```

## � **Model Caching**

PaddleOCR downloads models (~16MB total) on first use:
- `en_PP-OCRv3_det_infer.tar` (4MB) - Text detection  
- `en_PP-OCRv4_rec_infer.tar` (10MB) - Text recognition
- `ch_ppocr_mobile_v2.0_cls_infer.tar` (2MB) - Text orientation

### **Cache Benefits:**
- ✅ **Faster startup** - No download delays
- ✅ **Offline capable** - Works without internet after first download  
- ✅ **Bandwidth efficient** - Downloads once, uses forever

### **Cache Commands:**
```bash
# Pre-download models (run once after build)
make download-models

# Clean model cache if needed
make clean-models

# Check cache status
docker volume ls | grep paddleocr
```

## �🔧 Configuration

### Environment Variables

The Docker containers are configured with CPU-only settings:

- `CUDA_VISIBLE_DEVICES=""` - Disable GPU detection
- `OMP_NUM_THREADS=4` - OpenMP thread limit
- `MKL_NUM_THREADS=4` - Intel MKL thread limit

### Volume Mounts

- `./test_data` → `/app/input` (read-only)
- `./output` → `/app/output` (read-write)
- `./videos` → `/app/videos` (read-only, for video processing)

### Resource Limits

Default memory limits:
- Limit: 4GB
- Reservation: 2GB

## 🎯 Docker Compose Services

### Main Services

1. **plate-detector** - Single image processing (default)
2. **plate-detector-batch** - Batch processing (profile: batch)
3. **plate-detector-video** - Video processing (profile: video)

### Usage Examples

```bash
docker compose up -d plate-detector
```

## 🛠️ Makefile Commands

The `Makefile` provides convenient commands for all common tasks:

```bash
# Show available commands
make help

# Build and run
make build                        # Build Docker image
make dev-build                   # Build without cache
make quick-start                 # Build and run single detection

# Development
make shell                       # Interactive shell
make dev-shell                   # Development shell with mounted code
make test                        # Test CPU configuration
make info                        # Show system information
make run CMD="python --version"  # Run custom command

# Maintenance
make clean                       # Remove containers
make cleanup                     # Clean containers and system
make deep-clean                  # Remove everything
make show-output                 # Show output files
make clean-output               # Clean output directory

# Container management  
make ps                         # Show running containers
make logs                       # View logs
make stop                       # Stop containers
make restart                    # Restart containers
```

## 📝 Custom Commands

### Run Custom Detection Command


### Access Container Shell for Debugging

```bash
docker-compose run --rm plate-detector bash
# Inside container:
ls -la /app/
python --version
pip list
```

## 🔍 Troubleshooting

### Common Issues

1. **Permission Issues with Output Directory**
   ```bash
   chmod 755 output/
   sudo chown -R $USER:$USER output/
   ```


3. **Memory Issues**
   - Increase Docker memory allocation
   - Reduce image sizes or batch sizes

4. **Container Won't Start**
   ```bash
   make logs
   make clean
   make build
   ```

### Debugging Commands

```bash
# View container logs
make logs

# Check container status
make ps

# Show system information
make info

# Test configuration
make test

# Run custom debugging commands
make run CMD="env"
make run CMD="python -c 'import paddle; print(paddle.__version__)'"
```

## 🚀 Production Deployment

For production use:

1. **Build optimized image:**
   ```bash
   docker build -t plate-detector:prod --target production .
   ```

2. **Use external volumes:**
   ```yaml
   volumes:
     - /path/to/input:/app/input:ro
     - /path/to/output:/app/output:rw
   ```

3. **Configure resource limits:**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 8G
         cpus: '4.0'
   ```

## 📊 Performance Notes

- **CPU-only processing:** Slower than GPU but more compatible
- **Memory usage:** ~2-4GB depending on image size
- **Processing time:** 2-10 seconds per image (varies by CPU)
- **Batch processing:** More efficient for multiple images

## 🔗 Related Files

- `Dockerfile` - Container definition
- `docker-compose.yml` - Service orchestration
- `requirements.txt` - Python dependencies
- `.dockerignore` - Build optimization