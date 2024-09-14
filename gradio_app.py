import gradio as gr
import numpy as np
import asyncio
import websockets
import json
from scipy.signal import resample_poly

class ASRClient:
    def __init__(self):
        self.ws = None
        self.transcript = ''

    async def connect(self):
        try:
            self.ws = await websockets.connect('ws://localhost:6006')
            print('WebSocket connection established.')
            return True
        except Exception as e:
            print(f'Error connecting to WebSocket: {e}')
            self.ws = None
            return False

    async def send_audio(self, audio_data):
        if self.ws:
            try:
                await self.ws.send(audio_data.tobytes())
                # Receive transcription if available
                try:
                    message = await asyncio.wait_for(self.ws.recv(), timeout=0.1)
                    if isinstance(message, bytes):
                        message = message.decode('utf-8')
                    # Parse JSON response
                    data = json.loads(message)
                    text = data.get('text', '')
                    self.transcript = text
                except asyncio.TimeoutError:
                    pass  # No message received in time
                except json.JSONDecodeError:
                    print('Error decoding JSON from server response.')
            except Exception as e:
                print(f'WebSocket error: {e}')
                self.ws = None

    async def close(self):
        if self.ws:
            try:
                ws = self.ws
                self.ws = None
                await ws.close()
                print('WebSocket connection closed.')
            except Exception as e:
                print(f'Error closing WebSocket: {e}')

asr_client = ASRClient()

async def start_recording():
    # Attempt to open WebSocket connection
    success = await asr_client.connect()
    if not success:
        # Return an error message to display in the transcription box
        return 'Error: Failed to connect to ASR server.'
    else:
        asr_client.transcript = ''
        return ''  # Clear the transcription box

async def transcribe(audio_chunk):
    if asr_client.ws is None:
        return asr_client.transcript
    if audio_chunk is not None:
        sr, audio_data = audio_chunk
        audio_data = audio_data.astype(np.float32)

        # Resample to 16kHz if necessary
        if sr != 16000:
            audio_data = resample_poly(audio_data, up=16000, down=sr)

        # Normalize audio data
        max_abs = np.max(np.abs(audio_data))
        if max_abs > 0:
            audio_data = audio_data / max_abs

        await asr_client.send_audio(audio_data)
        return asr_client.transcript
    else:
        return asr_client.transcript

async def stop_recording():
    await asr_client.close()
    return asr_client.transcript  # Optionally return the final transcript

with gr.Blocks() as demo:
    transcript_box = gr.Textbox(label='Transcription')
    audio_input = gr.Audio(sources=['microphone'], streaming=True, label='Microphone Input')

    # Assign event handlers
    audio_input.start_recording(fn=start_recording, inputs=None, outputs=transcript_box)
    audio_input.stream(fn=transcribe, inputs=audio_input, outputs=transcript_box)
    audio_input.stop_recording(fn=stop_recording, inputs=None, outputs=transcript_box)

    demo.title = "Real-Time Streaming ASR with Gradio"
    demo.description = "Speak into your microphone and see the transcription in real-time."

demo.launch()
