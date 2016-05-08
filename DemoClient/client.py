#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.100', 5672, '/', credentials=pika.PlainCredentials('user', 'password')))

channel = connection.channel()

channel.exchange_declare(exchange='event.saveKeyValue',
                         type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='event.saveKeyValue',
                   queue=queue_name)

print(' [*] Waiting for events. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()

	
	


