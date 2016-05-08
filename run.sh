docker stop $(docker ps -a -q)

docker pull redis
docker pull rabbitmq

docker run -d --name redis-server -p 6379:6379 redis
docker run -d --name rabbitmq-server --hostname rabbitmq-server -e RABBITMQ_ERLANG_COOKIE='aleoEkdiwDFIEnjEE39322DECcsWPe' -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password -p 15672:15672 -p 5672:5672 rabbitmq:3-management
docker run -d benji:demoWorker
docker run -d -p 80:80 benji:demoApi
