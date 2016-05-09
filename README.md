# DemoSystem - A CQRS demo environment

Deployment: Docker, with bash scripts for building images and bringing up and tearing down environment.

Data Store: Redis.

Messaging: RabbitMQ.

DemoAPI: Python Flask API for data reads on GET / and GET /{key} and to send save command via GET /{key}/{value}.

DemoWorker: Python application that reads from command.saveKeyValue durable queue and performs data update on Redis.

DemoClient: HTML page that can call save API method and display events exposed over web via connection to RabbitMQ STOMP.

NOTE: IP address of docker host is hard coded in apps until I replace it with a shared config.
