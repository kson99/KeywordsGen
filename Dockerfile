# Use a slim, stable Python base image
FROM python:3.11-slim

# Set environment variables for stable container logs and execution
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install basic compiler tools required by some NLP dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# CRUCIAL: Pre-download the Hugging Face model during build time 
# This prevents slow initialization or runtime download failures inside production
RUN python -c "from keybert import KeyBERT; KeyBERT(model='all-MiniLM-L6-v2')"

# Copy your application script
COPY app.py .

# Expose FastAPI's default port
EXPOSE 8000

# Start KeyBERT with Uvicorn, listening on all network interfaces
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]