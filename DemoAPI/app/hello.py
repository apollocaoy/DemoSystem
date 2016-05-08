#!flask/bin/python
from flask import render_template
from flask import Flask
import redis
import pika
import json

app = Flask(__name__)

redisConn = redis.Redis('192.168.99.100', 6379)

@app.route('/<key>')
def get(key):	
	return redisConn.get(key)
	
@app.route('/<key>/<value>')
def save(key, value):	
	rabbitConn = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.100', 5672, '/', credentials=pika.PlainCredentials('user', 'password')))
	rabbitChannel = rabbitConn.channel()
	rabbitChannel.queue_declare(queue='command.saveKeyValue', durable=True)
	data = {}
	data['key'] = key
	data['value'] = value
	rabbitChannel.basic_publish(exchange='', routing_key='command.saveKeyValue', body=json.dumps(data)	, properties=pika.BasicProperties(delivery_mode=2))
	return "value submitted"

if __name__ == '__main__':
    app.run(debug=True)
