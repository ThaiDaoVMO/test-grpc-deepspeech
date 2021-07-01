curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./test.proto
