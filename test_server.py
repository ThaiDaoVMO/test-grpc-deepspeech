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
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from typing import Dict, TypedDict

import grpc

import test_pb2
import test_pb2_grpc

__all__ = "TestServer"

from speech_to_text import AudioChannel

SERVER_ADDRESS = "localhost:23333"
SERVER_ID = 1


def create_response(request: test_pb2.Request) -> test_pb2.Response:
    response = test_pb2.Response()
    response.id = request.id
    response.i = request.i + 1
    return response


class Phone(test_pb2_grpc.TestSSTStreamServicer):
    def __init__(self):
        self.count = 0
        self.stt_channel: Dict[int, AudioChannel] = {}

    def StreamCall(self, request_iterator, context):
        for request in request_iterator:
            if request.id not in self.stt_channel:
                self.stt_channel[request.id] = AudioChannel()
            stt_channel = self.stt_channel[request.id]
            stt_channel.recognize_audio(request.data_raw)
            yield test_pb2.Response(id=request.id, sentences=stt_channel.text_so_far)
            self.count += 1
            print(
                "recv from id(%d), data_raw= %s, count= %s"
                % (request.id, request.data_raw, self.count)
            )


def serve(address: str) -> None:
    server = grpc.server(ThreadPoolExecutor())
    test_pb2_grpc.add_TestSSTStreamServicer_to_server(Phone(), server)
    server.add_insecure_port(address)
    server.start()
    logging.info("Server serving at %s", address)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve(SERVER_ADDRESS)
