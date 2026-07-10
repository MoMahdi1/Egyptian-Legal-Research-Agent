FROM python:3.10-slim


# Set the working directory in the container
WORKDIR /app


# Update os packages and install python dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*


# Install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project 
COPY app/ ./app/
COPY data/ ./data/
COPY frontend/ ./frontend/


# Expose the port the app runs on
EXPOSE 8000 

# run FastAPI with uvicorn

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
