# Use an official Python runtime as the base image
FROM python:3.10.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg

# Copy the rest of the code to the container
COPY . .

# Run the command to start the bot
CMD ["python3", "Bot.py"]