import pika

server_loc = 'rabbitmq'  # use <yourip> instead
credentials = pika.PlainCredentials('guest', 'guest')
queue_name = 'TestQueue'
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672,
                                                               '/',
                                                               credentials))
# connection = pika.BlockingConnection(pika.ConnectionParameters(server_loc))
channel = connection.channel()
print('successfully connected to RabbitMQ server @ {}'.format(server_loc))

channel.queue_declare(queue=queue_name)
print('Connected to queue "{}"'.format(queue_name))


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

if __name__ == '__main__':
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
