# Use a Python base image with slim version
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file first and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Create /app directory if it doesn't exist
RUN mkdir -p /app

# Set the default command to run your application
CMD ["python", "app.py"]
