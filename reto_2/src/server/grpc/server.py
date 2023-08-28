from concurrent import futures
import grpc
import protobufs.python.FileServices_pb2 as FileServices_pb2
import protobufs.python.FileServices_pb2_grpc as FileServices_pb2_grpc
from common.services import Service

HOST = '[::]:50051'

class FileService(FileServices_pb2_grpc.FileServicesServicer):

    def ListFiles(self, request, context):
        print("Request is received: " + str(request))
        response = []

        for f in Service.listFiles():
            fileInfo = FileServices_pb2.FileInfo(name=f['name'],
                                                size=f['size'],
                                                timestamp=f['timestamp'])
            response.append(fileInfo)

        return FileServices_pb2.ListFilesResponse(file_info=response)

    def FindFile(self, request, context):
        print("Request Find Files is received: " + str(request))
        response = []

        for f in Service.findFiles(request.file_name):
            fileInfo = FileServices_pb2.FileInfo(name=f.name,
                                                size=f.size,
                                                timestamp=f.timestamp)
            response.append(fileInfo)

        return FileServices_pb2.FindFileResponse(files_info=response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    FileServices_pb2_grpc.add_FileServicesServicer_to_server(
        FileService(), server)
    server.add_insecure_port(HOST)
    print("Service is running... ")
    server.start()
    server.wait_for_termination()


def run():
    serve()
