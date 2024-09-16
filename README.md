# Real-Time Streaming ASR with Gradio and Sherpa-ONNX

This application provides real-time speech recognition through a Gradio web interface, utilizing a streaming ASR server powered by Sherpa-ONNX, and a pretrained ASR model.

## Video Demonstration

*Include a video link or embed demonstrating the application in action here.*

## Overview

Speak into your microphone and receive instant transcriptions of your speech in the browser. This application leverages:

- **Gradio**: For building the interactive web interface.
- **Sherpa-ONNX**: As the backend ASR server providing streaming speech recognition.

## Installation and Setup

### 1. Clone Repositories

Clone the Sherpa-ONNX repository:

git clone https://github.com/k2-fsa/sherpa-onnx.git

Clone or download this repository containing the Gradio app code.

### 2. Download the Pretrained Model

Download the **Streaming Zipformer English Model** from Sherpa-ONNX's pretrained models page:

- **Model Name**: `sherpa-onnx-streaming-zipformer-en-2023-06-26`

Extract the model files into a directory, e.g., `models/sherpa-onnx-streaming-zipformer-en-2023-06-26`.

### 3. Install Dependencies

Create a `requirements.txt` file with the following content:

gradio  
websockets  
numpy  
scipy  
torch  
torchvision  
torchaudio  
onnxruntime

Install the required Python packages:

pip install -r requirements.txt

### 4. Configure the ASR Server

Ensure the paths in the server script match the locations of your model files.

## Running the Application

### 1. Start the ASR Server

#### On Linux/MacOS

Create a script `run_asr_server.sh`:

#!/bin/bash

python3 sherpa-onnx/python-api-examples/streaming_server.py \
  --encoder models/sherpa-onnx-streaming-zipformer-en-2023-06-26/encoder-epoch-99-avg-1-chunk-16-left-128.onnx \
  --decoder models/sherpa-onnx-streaming-zipformer-en-2023-06-26/decoder-epoch-99-avg-1-chunk-16-left-128.onnx \
  --joiner models/sherpa-onnx-streaming-zipformer-en-2023-06-26/joiner-epoch-99-avg-1-chunk-16-left-128.onnx \
  --tokens models/sherpa-onnx-streaming-zipformer-en-2023-06-26/tokens.txt

Make it executable:

chmod +x run_asr_server.sh

Run the ASR server:

./run_asr_server.sh

#### On Windows

Create a batch script `run_asr_server.bat`:

python sherpa-onnx\python-api-examples\streaming_server.py ^
  --encoder models\sherpa-onnx-streaming-zipformer-en-2023-06-26\encoder-epoch-99-avg-1-chunk-16-left-128.onnx ^
  --decoder models\sherpa-onnx-streaming-zipformer-en-2023-06-26\decoder-epoch-99-avg-1-chunk-16-left-128.onnx ^
  --joiner models\sherpa-onnx-streaming-zipformer-en-2023-06-26\joiner-epoch-99-avg-1-chunk-16-left-128.onnx ^
  --tokens models\sherpa-onnx-streaming-zipformer-en-2023-06-26\tokens.txt

Run the ASR server:

run_asr_server.bat

### 2. Start the Gradio App

In a new terminal, run:

python gradio_app.py

This starts the Gradio interface and provides a local URL (e.g., `http://127.0.0.1:7860`).

## Usage

1. **Open the Gradio Interface**: Navigate to the URL provided in the terminal.

2. **Start Recording**: Click the microphone icon to begin.

3. **Speak**: Talk into your microphone. Partial transcriptions may appear.

4. **Stop Recording**: Click the microphone icon again. The final transcription will display after processing.

## Optional: Running with SSL Certificate

To run the ASR server with SSL for secure connections:

1. **Generate a Self-Signed Certificate**:

openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem

2. **Modify the ASR Server Script**:

Add `--certificate cert.pem --key key.pem` to your server script.

## Notes

- Ensure all paths in scripts match your directory structure.
- For detailed information on Sherpa-ONNX, refer to their GitHub repository: https://github.com/k2-fsa/sherpa-onnx

---

If you need any further adjustments or additional information, please let me know!
