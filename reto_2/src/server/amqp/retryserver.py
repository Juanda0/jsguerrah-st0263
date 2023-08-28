import json
import pika
import os
from common.services import Service

RMQ_HOST = os.getenv('RMQ_HOST')
RMQ_PORT = os.getenv('RMQ_PORT')
RMQ_USER = os.getenv('RMQ_USER')
RMQ_PASS = os.getenv('RMQ_PASS')

connection = pika.BlockingConnection(pika.ConnectionParameters(RMQ_HOST, RMQ_PORT, '/', pika.PlainCredentials(RMQ_USER, RMQ_PASS)))
channel = connection.channel()

def list_files(ch, method, properties, body):
    response = Service.listFiles()
    print(f'The response in LIST is : {response}')
    publish_response(ch, method, properties, response)

def find_files(ch, method, properties, body):
    response = Service.findFiles(body.decode('utf-8'))
    print(f'The response in FIND is : {response}')
    publish_response(ch, method, properties, response)

def publish_response(ch, method, properties, response):
    print("properties:", properties)
    print("Reply_to:", properties.reply_to)
    print("Corr_id:", properties.correlation_id)

    channel.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id,
        ),
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Response sent to RabbitMQ!")


def run():
    channel.basic_consume(queue="list_queue", on_message_callback=list_files, auto_ack=False)
    channel.basic_consume(queue="find_queue", on_message_callback=find_files, auto_ack=False)
    channel.start_consuming()
