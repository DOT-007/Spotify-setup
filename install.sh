#!/bin/bash

# Update package list and install ffmpeg
sudo apt-get update
sudo apt-get install -y ffmpeg

# Install spotdl
pip install spotdl

# Install pyTelegramBotAPI
pip install pyTelegramBotAPI


pip install -r req.txt



echo "Installation complete!"
