import gradio as gr
import requests
import numpy as np
import soundfile as sf

# Set chunk size and sample rate for Sherpa-onnx
CHUNK_SIZE = 50  # 50 ms chunks
SAMPLE_RATE = 16000  # Sherpa expects 16kHz

def send_audio_to_server(stream, new_chunk):
    sr, y = new_chunk  # Extract sample rate and audio data from chunk
    y = y.astype(np.float32)  # Convert to float32
    y /= np.max(np.abs(y))  # Normalize
    
    if stream is not None:
        stream = np.concatenate([stream, y])
    else:
        stream = y

    # Send audio data as HTTP POST request
    audio_data = stream.tobytes()
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post("https://localhost:6006", data=audio_data, headers=headers, verify=False)

    # Return the server response (the transcription)
    return stream, response.text

def transcribe(stream, new_chunk):
    return send_audio_to_server(stream, new_chunk)

# Gradio interface
demo = gr.Interface(
    fn=transcribe,
    inputs=["state", gr.Audio(sources=["microphone"], streaming=True)],
    outputs=["state", "text"],
    live=True,
)

demo.launch()
