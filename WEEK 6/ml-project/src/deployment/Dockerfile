FROM python:3.12-slim

WORKDIR /app

# Copy code
COPY ./api.py ./ 
COPY ../src/models ./src/models

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
