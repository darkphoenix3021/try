# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir: Disables the cache to reduce image size
# --trusted-host pypi.python.org: Sometimes needed in certain network environments or for older pip versions
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
# This assumes your Python script is named telegram_cli.py and is in the same directory as the Dockerfile
COPY telegram_cli.py .

# Make port 80 available to the world outside this container
# (Not strictly necessary for this CLI bot, but good practice if it were a web service)
# EXPOSE 80 

# Define environment variables (if any)
# ENV NAME World

# Run telegram_cli.py when the container launches
CMD ["python", "telegram_cli.py"]
