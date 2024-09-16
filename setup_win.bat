@echo off

REM Clone Sherpa-ONNX repository
echo Cloning Sherpa-ONNX repository...
git clone https://github.com/k2-fsa/sherpa-onnx.git

REM Download the pretrained model
echo Downloading the pretrained model...
mkdir sherpa-onnx\models
cd sherpa-onnx\models
curl -L -o sherpa-onnx-streaming-zipformer-en-2023-06-26.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-streaming-zipformer-en-2023-06-26.tar.bz2

REM Extract the model using tar
echo Extracting the pretrained model...
tar -xjf sherpa-onnx-streaming-zipformer-en-2023-06-26.tar.bz2
del sherpa-onnx-streaming-zipformer-en-2023-06-26.tar.bz2
cd ..\..

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

echo Setup complete.
pause
