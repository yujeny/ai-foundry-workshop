FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Copy startup script
COPY start.sh .
RUN chmod +x start.sh

# Start application with database initialization
CMD ["./start.sh"]
