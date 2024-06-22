# Use a Python base image with slim version
FROM python:3.9-slim


# Explicitly create /app directory if it doesn't exist (optional, for safety)
RUN mkdir -p /app

# Set the working directory in the container
WORKDIR /app

# Copy requirements file first and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set the default command to run your application
CMD ["python", "app.py"]
