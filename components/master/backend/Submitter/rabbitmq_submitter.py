from dotenv import load_dotenv
import os
import pika
import json

class RabbitMQSubmitter:
    def __init__(self,host_name,queue_name,port):
        self.host_name=host_name
        self.queue_name=queue_name
        self.port=port

    def submit(self, request):
        print(f" [x] Connecting to RabbitMQ at {self.host_name}, queue {self.queue_name}")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_name,port=self.port))        
        channel=connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_publish(exchange='', routing_key=self.queue_name, body=json.dumps(request))
        print(f" [x] Sent {request}")
        connection.close()