#!flask/bin/python
from flask import render_template
from flask import Flask
import redis
import pika
import json

app = Flask(__name__)

redisConn = redis.Redis('192.168.99.100', 6379)

@app.route('/')
def index():		
	list = []	
	for key in redisConn.scan_iter():
		value = redisConn.get(key)
		data = {}
		data['key'] = str(key, 'utf-8')
		data['value'] = str(value, 'utf-8')
		list.append(data)		
	print(list)
	return json.dumps(list)

@app.route('/<key>')
def get(key):	
	value = redisConn.get(key)
	data = {}
	data['key'] = key
	data['value'] = str(value, 'utf-8')
	return json.dumps(data)
	
@app.route('/<key>/<value>')
def save(key, value):	
	rabbitConn = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.100', 5672, '/', credentials=pika.PlainCredentials('user', 'password')))
	rabbitChannel = rabbitConn.channel()
	rabbitChannel.queue_declare(queue='command.saveKeyValue', durable=True)
	data = {}
	data['key'] = key
	data['value'] = value
	rabbitChannel.basic_publish(exchange='', routing_key='command.saveKeyValue', body=json.dumps(data)	, properties=pika.BasicProperties(delivery_mode=2))
	return json.dumps(data)
	
#@app.route('/', methods=['POST'])
#def post():
	#rabbitConn = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.100', 5672, '/', credentials=pika.PlainCredentials('user', 'password')))
	#rabbitChannel = rabbitConn.channel()
	#rabbitChannel.queue_declare(queue='command.saveKeyValue', durable=True)
	#data = {}
	#data['key'] = request.form['key'];
	#data['value'] = request.form['value'];
	#rabbitChannel.basic_publish(exchange='', routing_key='command.saveKeyValue', body=json.dumps(data)	, properties=pika.BasicProperties(delivery_mode=2))
	#return json.dumps(data)

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
	return response
  
if __name__ == '__main__':
    app.run(debug=True)
