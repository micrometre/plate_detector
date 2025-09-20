# Makefile for PaddleDetection UK License Plate Recognition
# ========================================================

.PHONY: help build video shell run dev-build dev-shell clean cleanup deep-clean ps stop restart show-output clean-output download-models clean-models

# Default target
.DEFAULT_GOAL := help

# Variables
IMAGE_NAME := plate-detector
CONTAINER_NAME := uk-plate-detector
DEFAULT_IMAGE := 1.jpg
DEFAULT_VIDEO := test_data/test_video.mp4

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
NC := \033[0m # No Color

# Help target
help: ## Show this help message
	@echo "$(BLUE)🐳 PaddleDetection UK License Plate Recognition - Docker Makefile$(NC)"
	@echo "$(BLUE)================================================================$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(CYAN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Examples:$(NC)"
	@echo "  $(YELLOW)make build$(NC)                    # Build Docker image"
	@echo "  $(YELLOW)make video VIDEO=my_video.mp4$(NC) # Process specific video"
	@echo "  $(YELLOW)make shell$(NC)                    # Interactive shell"

# Build Docker image
build: ## Build the Docker image
	@echo "$(GREEN)📦 Building Docker image...$(NC)"
	docker compose build
	@echo "$(GREEN)✅ Docker image built successfully!$(NC)"


# Process video file
video: ## Process video file (use VIDEO=filename.mp4 to specify)
	@echo "$(GREEN)🎬 Processing video: $(or $(VIDEO),test_video.mp4)$(NC)"
	docker compose run --rm $(IMAGE_NAME) \
		python deploy/pipeline/pipeline.py \
		--config deploy/pipeline/config/infer_cfg_ppvehicle.yml \
		--video_file "input/$(or $(VIDEO),test_video.mp4)" \
		--output_dir output \
		--send_to_api \
		--save_frames \
		--frame_skip 5

# Start interactive shell
shell: ## Start interactive bash shell in container
	@echo "$(GREEN)🖥️  Starting interactive shell...$(NC)"
	docker compose run --rm $(IMAGE_NAME) bash

# Custom command runner
run: ## Run custom command in container (use CMD="your command")
ifndef CMD
	@echo "$(RED)❌ Error: CMD variable is required$(NC)"
	@echo "$(YELLOW)Example: make run CMD=\"python --version\"$(NC)"
else
	@echo "$(GREEN)🔧 Running custom command: $(CMD)$(NC)"
	docker compose run --rm $(IMAGE_NAME) $(CMD)
endif

# Development targets
dev-build: ## Build image without cache (for development)
	@echo "$(GREEN)🔨 Building Docker image without cache...$(NC)"
	docker compose build --no-cache
	@echo "$(GREEN)✅ Docker image built successfully!$(NC)"

dev-shell: ## Start development shell with mounted source code
	@echo "$(GREEN)🛠️  Starting development shell...$(NC)"
	docker compose run --rm -v $(PWD):/app/src $(IMAGE_NAME) bash

# Cleanup targets
clean: ## Remove containers and images
	@echo "$(YELLOW)🧹 Cleaning up containers...$(NC)"
	docker compose down
	@echo "$(GREEN)✅ Containers stopped and removed$(NC)"

cleanup: clean ## Alias for clean
	@echo "$(YELLOW)🧹 Cleaning up Docker system...$(NC)"
	docker system prune -f
	@echo "$(GREEN)✅ Cleanup completed!$(NC)"

deep-clean: ## Remove everything including images and volumes
	@echo "$(RED)⚠️  Performing deep clean - this will remove images and volumes$(NC)"
	docker compose down -v --rmi all
	docker system prune -af --volumes
	@echo "$(GREEN)✅ Deep cleanup completed!$(NC)"

# Utility targets
ps: ## Show running containers
	@docker compose ps

stop: ## Stop all running containers
	@echo "$(YELLOW)⏹️  Stopping containers...$(NC)"
	docker compose stop

restart: ## Restart containers
	@echo "$(YELLOW)🔄 Restarting containers...$(NC)"
	docker compose restart

# Output management
show-output: ## Show recent output files
	@echo "$(GREEN)📁 Recent output files:$(NC)"
	@ls -la output/ | head -10 || echo "No output files found"

clean-output: ## Clean output directory
	@echo "$(YELLOW)🗑️  Cleaning output directory...$(NC)"
	@rm -rf output/*
	@echo "$(GREEN)✅ Output directory cleaned$(NC)"

# Model management
download-models: ## Pre-download PaddleOCR models to cache
	@echo "$(GREEN)📥 Pre-downloading PaddleOCR models...$(NC)"
	docker compose run --rm $(IMAGE_NAME) python -c "\
import paddleocr; \
print('Initializing PaddleOCR to download models...'); \
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='en'); \
print('✅ Models cached successfully!')"

clean-models: ## Clean cached PaddleOCR models
	@echo "$(YELLOW)🗑️  Cleaning PaddleOCR model cache...$(NC)"
	docker volume rm plate-detector_paddleocr-models 2>/dev/null || true
	@echo "$(GREEN)✅ Model cache cleaned$(NC)"
