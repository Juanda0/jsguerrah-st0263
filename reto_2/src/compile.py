import subprocess

def compile_proto(proto_file_path, output_dir):
    try:
        command = ["python3", "-m", "grpc_tools.protoc", "-I", proto_dir, f"--python_out={output_dir}", f"--pyi_out={output_dir}", f"--grpc_python_out={output_dir}", proto_file_path]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print("Archivo .proto compilado exitosamente.")
        else:
            print("Error al compilar el archivo .proto:")
            print(result.stderr)
    except Exception as e:
        print("Ocurrió un error:", str(e))

proto_dir = "./protobufs/proto"
proto_file = "./protobufs/proto/FileServices.proto"
output_directory = "./protobufs/python"
compile_proto(proto_file, output_directory)
