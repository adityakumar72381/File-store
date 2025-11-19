FROM python:3.10-slim

# Update system packages
RUN apt update && apt upgrade -y

# Copy requirements
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r /requirements.txt

# Working directory
WORKDIR /file-store-bot

# Copy project files
COPY . /file-store-bot

# Start the bot
CMD ["python3", "bot.py"]
