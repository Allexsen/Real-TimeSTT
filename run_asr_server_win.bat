python sherpa-onnx\python-api-examples\streaming_server.py ^
  --encoder models\sherpa-onnx-streaming-zipformer-en-2023-06-26\encoder-epoch-99-avg-1-chunk-16-left-128.onnx ^
  --decoder models\sherpa-onnx-streaming-zipformer-en-2023-06-26\decoder-epoch-99-avg-1-chunk-16-left-128.onnx ^
  --joiner models\sherpa-onnx-streaming-zipformer-en-2023-06-26\joiner-epoch-99-avg-1-chunk-16-left-128.onnx ^
  --tokens models\sherpa-onnx-streaming-zipformer-en-2023-06-26\tokens.txt