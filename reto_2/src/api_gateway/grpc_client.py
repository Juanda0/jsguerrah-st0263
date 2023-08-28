
import grpc
from protobufs.python.FileServices_pb2_grpc import FileServicesStub
import os

GRPC_HOST = os.getenv('GRPC_HOST')

channel = grpc.insecure_channel(GRPC_HOST)
stub = FileServicesStub(channel=channel)
