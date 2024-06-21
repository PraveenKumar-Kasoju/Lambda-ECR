# Use the official AWS Lambda Python 3.8 base image
FROM public.ecr.aws/lambda/python:3.8

# Copy the function code into the container at /var/task
COPY app.py ${LAMBDA_TASK_ROOT}

# Optionally, install additional Python dependencies
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Set the command to your handler function
CMD ["app.lambda_handler"]
