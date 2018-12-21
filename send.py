#!/usr/bin/env python
import pika


server_loc = 'rabbitmq'  # use <yourip> instead
credentials = pika.PlainCredentials('guest', 'guest')
queue_name = 'TestQueue'
body = "This is the first message"

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672,
                                                               '/',
                                                               credentials))
# connection = pika.BlockingConnection(pika.ConnectionParameters(server_loc))
channel = connection.channel()
print('successfully connected to RabbitMQ server @ {}'.format(server_loc))

channel.queue_declare(queue=queue_name)
print('Created queue "{}"'.format(queue_name))

channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body=body)
print(' [x] Sent "{}"'.format(body))

connection.close()
print('Connection closed')