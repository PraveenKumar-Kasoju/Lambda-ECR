# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app.py

# Copy requirements file first and install dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application to the container's working directory
COPY . .

# Create /app directory if it doesn't exist (though typically unnecessary if using COPY . .)
RUN mkdir -p /app.py

# Expose the port Flask runs on
EXPOSE 5000

# Set the default command to run when a container starts
CMD ["python", "app.py"]
