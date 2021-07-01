# Copyright 2020 The gRPC Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import threading
import time
from typing import Iterator
from concurrent.futures import ThreadPoolExecutor

import grpc

import test_pb2
import test_pb2_grpc
from speech_to_text import AudioChannel

__all__ = "TestServer"
SERVER_ADDRESS = "localhost:23333"
SERVER_ID = 1


def bidirectional_streaming_method(stub, id):
    print("--------------Call BidirectionalStreamingMethod Begin---------------")

    def request_messages():
        print(11111111)
        audio_channel = AudioChannel()
        print(2222)
        while True:
            if audio_channel.data_raw:
                data_raw = audio_channel.data_raw.pop(0)
                send_data = test_pb2.Request(id=id, data_raw=data_raw)
                yield send_data
            # time.sleep(1)

    response_iterator = stub.StreamCall(request_messages())
    print(response_iterator)
    for response in response_iterator:
        print("recv from id(%d), i=%s" % (response.id, response.sentences))
    print("--------------Call BidirectionalStreamingMethod Over---------------")


def main():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = test_pb2_grpc.TestSSTStreamStub(channel)

        bidirectional_streaming_method(stub, 2)


if __name__ == "__main__":
    main()
