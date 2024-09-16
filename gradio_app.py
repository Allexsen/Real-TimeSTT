import gradio as gr
import numpy as np
import asyncio
import websockets
import json
from scipy.signal import resample_poly

class ASRClient:
    """
    Client for streaming audio data to an ASR server and receiving transcriptions.

    Attributes:
        ws (websockets.client.WebSocketClientProtocol): WebSocket connection to the ASR server.
        transcript (str): Current transcription received from the server.
    """

    def __init__(self):
        self.ws = None
        self.transcript = ''

    async def connect(self):
        """
        Establish a WebSocket connection to the ASR server.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """
        try:
            self.ws = await websockets.connect('ws://localhost:6006')
            print('WebSocket connection established.')
            self.transcript = ''
            return True
        except Exception as e:
            print(f'Error connecting to WebSocket: {e}')
            self.ws = None
            return False

    async def send_audio(self, audio_data):
        """
        Send audio data to the ASR server and receive partial transcriptions.

        Args:
            audio_data (np.ndarray): Audio data to send.
        """
        if self.ws is None:
            return
        try:
            await self.ws.send(audio_data.tobytes())
            message = await asyncio.wait_for(self.ws.recv(), timeout=0.1)

            if isinstance(message, bytes):
                message = message.decode('utf-8')
            
            data = json.loads(message)
            self.transcript = data.get('text', '')
        
        except (asyncio.TimeoutError, json.JSONDecodeError):
            pass  # Ignore timeout and JSON decoding errors
        except Exception as e:
            print(f'WebSocket error: {e}')
            self.ws = None

    async def finish(self):
        """
        Finalize the streaming session by sending tail padding and a "Done" message,
        then receive the final transcription from the server.
        """
        if self.ws is None:
            return
        try:
            tail_padding = np.zeros(int(16000 * 0.5), dtype=np.float32)
            await self.ws.send(tail_padding.tobytes())
            await self.ws.send('Done')

            while True:
                try:
                    message = await asyncio.wait_for(self.ws.recv(), timeout=1.0)
                    if isinstance(message, bytes):
                        message = message.decode('utf-8')
                    data = json.loads(message)
                    self.transcript = data.get('text', '')
                    print(f'Received final transcription: {self.transcript}')
                except (asyncio.TimeoutError, json.JSONDecodeError):
                    break # Ignore timeout and JSON decoding errors
                except websockets.exceptions.ConnectionClosedOK:
                    print('WebSocket connection closed by server.')
                    break
            
            if self.ws.open:
                await self.ws.close()
            print('WebSocket connection closed.')
            self.ws = None
        except Exception as e:
            print(f'Error during finish: {e}')
            self.ws = None

asr_client = ASRClient()

async def start_recording():
    """
    Event handler for starting the recording session.
    Connects to the ASR server and clears the transcription box.

    Returns:
        str: An empty string to clear the transcription box, or an error message.
    """
    success = await asr_client.connect()
    return '' if success else 'Error: Failed to connect to ASR server.'

async def transcribe(audio_chunk):
    """
    Event handler for streaming audio chunks to the ASR server.

    Args:
        audio_chunk (tuple): Tuple containing the sample rate and audio data.

    Returns:
        str: The current transcription.
    """
    if asr_client.ws is None or audio_chunk is None:
        return asr_client.transcript

    sr, audio_data = audio_chunk
    audio_data = audio_data.astype(np.float32)

    if sr != 16000:
        audio_data = resample_poly(audio_data, up=16000, down=sr)
    max_abs = np.max(np.abs(audio_data))
    if max_abs > 0:
        audio_data /= max_abs
    
    await asr_client.send_audio(audio_data)
    return asr_client.transcript

async def stop_recording():
    """
    Event handler for stopping the recording session.
    Finalizes the streaming session and returns the final transcription.

    Returns:
        str: The final transcription.
    """
    await asr_client.finish()
    return asr_client.transcript

with gr.Blocks() as demo:
    transcript_box = gr.Textbox(label='Transcription')
    audio_input = gr.Audio(sources=['microphone'], streaming=True, label='Microphone Input')

    audio_input.start_recording(fn=start_recording, inputs=None, outputs=transcript_box)
    audio_input.stream(fn=transcribe, inputs=audio_input, outputs=transcript_box)
    audio_input.stop_recording(fn=stop_recording, inputs=None, outputs=transcript_box)
    
    demo.title = "Real-Time Streaming ASR with Gradio"
    demo.description = "Speak into your microphone and see the transcription in real-time."

demo.launch()
