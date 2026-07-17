.PHONY: help install run build clean docker-build docker-up docker-down docker-logs

help:
	@echo "Video Downloader API - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install          - Install dependencies"
	@echo "  make run              - Run the application locally"
	@echo "  make clean            - Clean up virtual environment and cache"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-up        - Start containers with docker-compose"
	@echo "  make docker-down      - Stop and remove containers"
	@echo "  make docker-logs      - View container logs"
	@echo ""

install:
	python -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && python app.py

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

docker-build:
	docker build -t video-downloader-api:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f video-downloader
