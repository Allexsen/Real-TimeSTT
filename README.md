# Real-Time Streaming ASR with Gradio and Sherpa-ONNX

This application provides real-time speech recognition through a Gradio web interface, utilizing a streaming ASR server powered by Sherpa-ONNX, and a pretrained ASR model.

## Video Demonstration

*TODO: The video link*

## Overview

Real-time Speech-to-Text web app using gradio, taking input from a microphone and displaying transcription of the spoken speech. This application leverages:

- **Gradio**: For building the interactive web interface.
- **Sherpa-ONNX**: As the backend ASR server providing streaming speech recognition.
- **Pretrained ASR model**: [Sherpa-onnx-streaming-zipformer-en](https://k2-fsa.github.io/sherpa/onnx/pretrained_models/online-transducer/zipformer-transducer-models.html#csukuangfj-sherpa-onnx-streaming-zipformer-en-2023-06-26-english)

The given model is optional and you can change it to your will, but you will have to modify the code accordingly to your model's behavior, files structure, etc.

## Cloning this repo

To clone this repo, run the command in your terminal:
```bash
git clone https://github.com/Allexsen/Real-TimeSTT
```

## Automated Setup

To automate the setup process, run the setup script for your operating system:

Linux/MacOS:
```bash
./setup.sh
```

Windows:
```bash
setup.bat
```

## Manual Setup

### 1. Clone Repositories

Clone the Sherpa-ONNX repository:
```bash
git clone https://github.com/k2-fsa/sherpa-onnx.git
```

Clone or download this repository containing the Gradio app code.

### 2. Download the Pretrained Model

Download the **[Sherpa-onnx-streaming-zipformer-en](https://k2-fsa.github.io/sherpa/onnx/pretrained_models/online-transducer/zipformer-transducer-models.html#csukuangfj-sherpa-onnx-streaming-zipformer-en-2023-06-26-english)** from Sherpa-ONNX's pretrained models page:

Linux/MacOS:
```bash
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-streaming-zipformer-en-2023-06-26.tar.bz2
```
Windows:
```bash
curl -o https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-streaming-zipformer-en-2023-06-26.tar.bz2
```

Extract the model files into a directory, e.g., `models/sherpa-onnx-streaming-zipformer-en-2023-06-26`. Note that you will have to adjust the `run_asr_server` paths accordingly if you decide to extract it any other way.

### 3. Install Dependencies

Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Configure the ASR Server

Ensure the paths in the server script match the locations of your model files.

## Running the Application

### 1. Start the ASR Server

Linux/MacOS:
```bash
./run_asr_server_lin.sh
```

Windows:
```bash
run_asr_server_win.bat
```

### 2. Start the Gradio App

In a new terminal, run:
```bash
python gradio_app.py
```

This starts the Gradio interface and provides a local URL (e.g., `http://localhost:7860`).

You can combine the ASR server and the gradio app running scripts, however mismatch in their starting times might cause WebSocket connnection issues when trying to transcribe via Gradio app if the ASR server hasn't started yet.

## Usage

1. **Open the Gradio Interface**: Navigate to the URL provided in the terminal.

2. **Start Recording**: Click the microphone icon to begin.

3. **Speak**: Talk into your microphone. Partial transcriptions may appear.

4. **Stop Recording**: Click the microphone icon again. The final transcription will display after processing.

## Optional: Running with SSL Certificate

To run the ASR server with SSL for secure connections:

1. **Generate a Self-Signed Certificate**:

 Navigate to the `python-api-examples/web` directory within the Sherpa-ONNX repository and run the certificate generation script:

 ```bash
 cd sherpa-onnx/python-api-examples/web
 ./generate-certificate.py
 cd ../..
```

2. **Modify the ASR Server Script**:

Add `--certificate cert.pem --key key.pem` to your server script.

The full script will now look like:
```bash
cd ./sherpa-onnx
python3 python-api-examples/streaming_server.py \
  --encoder ./models/sherpa-onnx-streaming-zipformer-en-2023-06-26/encoder-epoch-99-avg-1-chunk-16-left-128.onnx \
  --decoder ./models/sherpa-onnx-streaming-zipformer-en-2023-06-26/decoder-epoch-99-avg-1-chunk-16-left-128.onnx \
  --joiner ./models/sherpa-onnx-streaming-zipformer-en-2023-06-26/joiner-epoch-99-avg-1-chunk-16-left-128.onnx \
  --tokens ./models/sherpa-onnx-streaming-zipformer-en-2023-06-26/tokens.txt \
--certificate ./python-api-examples/web/cert.pem
```

## Notes

- Ensure all paths in scripts match your directory structure.
- For detailed information on Sherpa-ONNX, refer to their GitHub repository: https://github.com/k2-fsa/sherpa-onnx
