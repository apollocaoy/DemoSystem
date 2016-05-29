#!/usr/bin/env python
from flask import Flask, abort, make_response, request
import redis
import pika
import json

app = Flask(__name__)

redisConn = redis.Redis('192.168.99.100', 6379)

rabbitConn = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.100', 5672, '/', credentials=pika.PlainCredentials('user', 'password')))

rabbitChannel = rabbitConn.channel()

rabbitChannel.queue_declare(queue='command.saveKeyValue', durable=True)

@app.route('/')
def index():

	dataList = []

	for key in redisConn.scan_iter():

		value = redisConn.get(key)

		if value is not None:

			data = {}
			data['key'] = str(key, 'utf-8')
			data['value'] = str(value, 'utf-8')

		dataList.append(data)

	return make_response(json.dumps(dataList), 200)

@app.route('/<key>')
def get(key):

	value = redisConn.get(key)

	if value is None:

		abort(404)

	data = {}
	data['key'] = key
	data['value'] = str(value, 'utf-8')

	return make_response(json.dumps(data), 200)

@app.route('/<key>/<value>')
def save(key, value):

	data = {}
	data['key'] = key
	data['value'] = value

	rabbitChannel.basic_publish(exchange='', routing_key='command.saveKeyValue', body=json.dumps(data), properties=pika.BasicProperties(delivery_mode=2))

	return make_response(json.dumps(data), 201)

@app.route('/', methods=['POST'])
def post():

	data = request.json

	rabbitChannel.basic_publish(exchange='', routing_key='command.saveKeyValue', body=json.dumps(data), properties=pika.BasicProperties(delivery_mode=2))

	return make_response(json.dumps(data), 201)


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
