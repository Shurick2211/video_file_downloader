FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app.py .
COPY download_service.py .

# Expose port
EXPOSE 9001

# Run the application
CMD ["python", "app.py"]
