#!/bin/bash
# Setup script for PaddleDetection Vehicle License Plate Recognition (CPU Version)
# This script creates a virtual environment and installs CPU-only dependencies

set -e

echo "🖥️  Setting up PaddleDetection Vehicle License Plate Recognition (CPU Version)..."
echo "=================================================================="

# Disable CUDA to force CPU usage
export CUDA_VISIBLE_DEVICES=""
echo "🚫 CUDA disabled - forcing CPU-only mode"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv
echo "✅ Virtual environment created in .venv/"

# Activate virtual environment
source .venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements (CPU-only versions)
echo "📥 Installing CPU-only Python dependencies..."
pip install -r requirements.txt

# Create CPU configuration script
echo "⚙️  Creating CPU configuration..."
cat > cpu_config.sh << 'EOF'
#!/bin/bash
# CPU Configuration for PaddleDetection
export CUDA_VISIBLE_DEVICES=""
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
echo "🖥️  CPU-only mode configured"
EOF

chmod +x cpu_config.sh

echo ""
echo "🎉 Setup completed successfully (CPU Version)!"
echo "=================================================================="
echo ""
echo "🚀 To use the environment:"
echo "1. Activate virtual environment: source .venv/bin/activate"
echo "2. Configure CPU mode: source cpu_config.sh"
echo "3. Run license plate detection:"
echo "   python deploy/pipeline/pipeline.py --config deploy/pipeline/config/infer_cfg_ppvehicle.yml --image_file test_data/1.jpg"
echo ""
echo "💡 Example commands:"
echo "# Setup and single image"
echo "source .venv/bin/activate && source cpu_config.sh"
echo "python deploy/pipeline/pipeline.py --config deploy/pipeline/config/infer_cfg_ppvehicle.yml --image_file test_data/1.jpg"
echo ""
echo "# Multiple images"
echo "python deploy/pipeline/pipeline.py --config deploy/pipeline/config/infer_cfg_ppvehicle.yml --image_dir test_data/"
echo ""
echo "⚠️  Note: CPU processing will be slower than GPU but more compatible"
echo "🔧 Deactivate environment when done: deactivate"
