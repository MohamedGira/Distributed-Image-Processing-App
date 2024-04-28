from dotenv import load_dotenv
import os
import pika

class RabbitMQSubmitter:
    def __init__(self,host_name,queue_name):
        self.host_name=host_name
        self.queue_name=queue_name

    def submit(self, request):
        channel = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_name)).channel()
        channel.queue_declare(queue=self.queue_name)
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=request)
        print(f" [x] Sent {request}")
        self.connection.close()