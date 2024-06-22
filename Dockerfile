# Use an official Python runtime as a parent image (3.8 recommended for compatibility)
FROM python:3.8-slim

# Set working directory in the container (optional, depends on your project structure)
# This line can be removed if your application code is already at the root of the context
WORKDIR /app

# Copy the current directory contents (excluding unnecessary files) into the container at /app
COPY . . --from=source

# Define a multi-stage build for a smaller final image
# Stage 1: Install dependencies
STAGE build
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Copy application code and set entrypoint
FROM python:3.8-slim AS final
COPY --from=source . .
WORKDIR /app  # Optional, if not set earlier

# Expose port if your application needs it (replace 8000 with your port)
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "app.py"]
