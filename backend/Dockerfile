# Backend Dockerfile - Production Optimized
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt /app/
# Copy phase_iii requirements (fixed path)
COPY phase_iii/requirements.txt /app/phase_iii/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r phase_iii/requirements.txt \
    && pip install uvicorn[standard]

# Copy backend source
COPY backend /app/backend/
# Copy phase_iii source (required for Agent logic)
COPY phase_iii /app/phase_iii/

# Chown all files to the app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Set working directory to backend
WORKDIR /app/backend

# CMD to run the backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
