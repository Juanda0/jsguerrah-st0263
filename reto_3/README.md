# Service communication project


## Course Details


| Information  |                   |
|--------------|      :-----:      |
| Name    | Sebastian Guerra       |
| Email   | jsguerrah@eafit.edu.co |
| Teacher | Edwin Montoya          |
| Course  | ST0263                 |

## Description

This project was created to practice both synchronous and asynchronous communication strategies. For this we set up an API that makes available two microservices to list and search for files

The information and parameters of the project criteria are in the teacher's domain. In view of this situation, it remains to say that in this project all the considerations required by the teacher are completely fulfilled.
## Run by your own

- Start docker container for RabbitMQ in its respective instance.

```bash
  docker start rabbit-server
```

- Clone the project

```bash
  git clone https://github.com/Jguerra47/jsguerrah-st0263.git
```

- Go to the project directory

```bash
  cd jsguerrah-st0263/reto_2/src
```

- Install dependencies

```bash
  pip install -r requirements.txt
```

- Set the environment variables cloning the `.env.example`

```bash
  mv config/.env.example config/.env
```

- Check if stubs are created. If you need to modify the IDL, re-compile it with

```bash
  python3 compile.py
```

- Run the component according to the instance. To know components use `--help` flag

```bash
  python3 main.py {component}
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file in **config** folder

`GRPC_HOST`
`RMQ_HOST`
`RMQ_PORT`
`RMQ_USER`
`RMQ_PASS`
`RMQ_EXCHANGE`

## Directory tree
```bash
    reto_2/
    │
    ├── src/
    │   ├── compile.py
    │   ├── main.py
    │   ├── requirements.txt
    │   │
    │   ├── api_gateway/
    │   │
    │   ├── server/
    │   │   ├── amqp/
    │   │   ├── common/
    │   │   └── grpc/
    │   │
    │   ├── protobufs/
    │   │   ├── python/
    │   │   └── proto/
    │   │
    │   └── config/
    │
    └── assets/
        ├── [contenido de assets...]
```
## API Gateway Reference

#### Get all items:

```http
  curl --location '${API_GW_HOST}/list'
```

#### Find items by a string:

```http
  curl --location '${API_GW_HOST}/find/${name}'
```

# Tech description

## Diagram

![CommunicationProjectDiagram](https://github.com/Jguerra47/jsguerrah-st0263/assets/68879896/ad116a72-dc5b-47d7-a1f0-95ee725c235d)

## Development environment

### Language
- **Python**

### Libraries and packages
- **grpcio**: 1.57.0
- **grpcio-tools**: 1.57.0
- **protobuf**: 4.24.2
- **pika**: 1.2.0
- **flask**: 2.0.1
- **flask-restful**: 0.3.9
- **python-dotenv**: 0.17.1

## High Level Design and Architecture

The project uses **Flask** as a web framework to create an API. In addition, **gRPC** is used for communication between backend services as well as **AMQP** for message publishing as a retry strategy since `RabbitMq` is used as Message-Oriented Middleware. The code structure suggests a clear separation of responsibilities, with specific files for gateway configuration, gRPC communication, AMQP queue management, and resource and route definition.

### Patterns and practices

- **RPC client**: The project defines an RPC client `AMQPRpcClient` with an AMQP server. This, to simulate a synchronous communication with the MOM.

- **Separation of Responsibilities**: There is a clear distinction between different aspects of the system, such as route management, resources, gRPC communication and AMQP queues.

- **Dependency Management**: `requirements.txt` is used to manage project dependencies.

- **Environment-Based Configuration**: Environment variables are used for configurations, suggesting an environment-based configuration approach.

- **Modular Organization**: The code is organized in a modular fashion with a clear and defined directory structure for recognition of each aspect of the design.
## Response snapshots

<img width="451" alt="image" src="https://github.com/Jguerra47/jsguerrah-st0263/assets/68879896/bc3bcd09-d8b9-4232-9b9b-f315ec30ff96">

## Check IPs
Click [here](https://github.com/Jguerra47/jsguerrah-st0263/tree/main/reto_2/src/config)

## Functionality Demo
Access to a video that explains the project and test it. Click [here](https://drive.google.com/file/d/1lkoMbLLo_4g6_JrnPRfvipHvjW-7xCEZ/view?usp=sharing)

## References

- [RabbitMQ documentation](https://www.rabbitmq.com/getstarted.html)
- [Python + gRPC](https://www.youtube.com/watch?v=E0CaocyNYKg)
- [Message-Oriented Middleware](https://www.geeksforgeeks.org/what-is-message-oriented-middleware-mom/)
- [Flask documentation](https://flask.palletsprojects.com/en/2.3.x/)
