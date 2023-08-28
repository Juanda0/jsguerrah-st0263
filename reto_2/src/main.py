import argparse

# Configura el parser de argumentos
parser = argparse.ArgumentParser(
    description='Ejecuta componentes del proyecto. Puede ser el servidor, el servidor de retry o el gateway.')

parser.add_argument('component',
                    type=str,
                    choices=['server','retry', 'gateway'],
                    help='Especifica el componente a ejecutar. "server" para correr el servidor, "retry" para correr el servidor de reintento "y "gateway" para el api-gateway.')

args = parser.parse_args()

if args.component == 'server':
    from server.grpc import server
    server.run()
elif args.component == 'retry':
    from server.amqp import retryserver
    retryserver.run()
elif args.component == 'gateway':
    from api_gateway import gateway
    gateway.run()
