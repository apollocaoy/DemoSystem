import redis
import pika
import json

print(' [*] Initialising command consumer')

redisConn = redis.Redis('192.168.99.100', 6379)

rabbitConn = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.100', 5672, '/', credentials=pika.PlainCredentials('user', 'password')))

rabbitChannel = rabbitConn.channel()

rabbitChannel.queue_declare(queue='command.saveKeyValue', durable=True)

rabbitChannel.exchange_declare(exchange='event.saveKeyValue', type='fanout')

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	
	print(" [x] Received %r" % str(body, 'utf-8'))
	
	data = json.loads(str(body, 'utf-8'))
	
	redisConn.set(data['key'], data['value'])
	
	print(" [x] Value updated")
	
	ch.basic_ack(delivery_tag = method.delivery_tag)
	
	print(" [x] ACK sent")
		
	ch.basic_publish(exchange='event.saveKeyValue', routing_key='', body=body)
	
	print(" [x] Notification published")
	

rabbitChannel.basic_qos(prefetch_count=1)

rabbitChannel.basic_consume(callback, queue='command.saveKeyValue')

rabbitChannel.start_consuming()
