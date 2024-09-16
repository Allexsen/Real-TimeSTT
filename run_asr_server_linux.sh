#!/bin/bash

# Clone Sherpa-ONNX repository
echo "Cloning Sherpa-ONNX repository..."
git clone https://github.com/k2-fsa/sherpa-onnx.git

# Download the pretrained model
echo "Downloading the pretrained model..."
mkdir -p sherpa-onnx/models
cd sherpa-onnx/models
wget -O sherpa-onnx-streaming-zipformer-en-2023-06-26.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-streaming-zipformer-en-2023-06-26.tar.bz2

# Extract the model
echo "Extracting the pretrained model..."
tar -xjf sherpa-onnx-streaming-zipformer-en-2023-06-26.tar.bz2
rm sherpa-onnx-streaming-zipformer-en-2023-06-26.tar.bz2
cd ../../

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup complete."
