import gradio as gr
import numpy as np
import asyncio
import websockets
import json
from scipy.signal import resample_poly

async def transcribe(state, new_chunk):
    if new_chunk is None:
        # Recording has stopped
        if state.get('ws') is not None:
            try:
                print("Sending 'Done' message and closing WebSocket...")
                await state['ws'].send("Done")
                await state['ws'].close()
                state['ws'] = None
                # When recording stops, add current_transcript to cumulative_transcript
                state['cumulative_transcript'] += state.get('current_transcript', '')
                state['current_transcript'] = ''
                print("WebSocket connection closed.")
            except Exception as e:
                print(f"Error closing websocket: {e}")
        return state, state.get('transcript', '')
    else:
        sr, y = new_chunk
        y = y.astype(np.float32)

        # Resample from sr (likely 48000Hz) to 16000Hz
        if sr != 16000:
            # Resample
            y = resample_poly(y, up=16000, down=sr)

        # Normalize the audio data
        max_abs_y = np.max(np.abs(y))
        if max_abs_y > 0:
            y = y / max_abs_y

        if state.get('ws') is None:
            # Initialize and establish websocket connection
            try:
                print("Establishing WebSocket connection...")
                state['ws'] = await websockets.connect('ws://localhost:6006')
                state['current_transcript'] = ''  # Reset current transcript
                print("WebSocket connection established.")
            except Exception as e:
                print(f"Error connecting to websocket: {e}")
                return state, state.get('transcript', '')

        try:
            # Send audio data
            await state['ws'].send(y.tobytes())

            # Receive transcription
            # Use asyncio.wait_for to prevent blocking indefinitely
            try:
                message = await asyncio.wait_for(state['ws'].recv(), timeout=0.1)
                # The message may be JSON
                if isinstance(message, bytes):
                    message = message.decode('utf-8')
                # Parse JSON if necessary
                try:
                    data = json.loads(message)
                    text = data.get('text', '')
                except json.JSONDecodeError:
                    text = message
                print(f"Received transcription: {text}")
                # Update current transcript
                state['current_transcript'] = text
                # Update overall transcript
                state['transcript'] = state.get('cumulative_transcript', '') + state.get('current_transcript', '')
            except asyncio.TimeoutError:
                # No message received in time
                pass
        except Exception as e:
            print(f"Websocket error: {e}")
            state['ws'] = None

        return state, state.get('transcript', '')

with gr.Blocks() as demo:
    # Initialize state with cumulative_transcript and current_transcript
    state = gr.State({
        'ws': None,
        'transcript': '',
        'current_transcript': '',
        'cumulative_transcript': ''
    })
    txt = gr.Textbox(label="Transcription")

    with gr.Row():
        audio = gr.Audio(sources=["microphone"], streaming=True, label="Microphone Input")

    audio.stream(fn=transcribe, inputs=[state, audio], outputs=[state, txt])

demo.launch()
