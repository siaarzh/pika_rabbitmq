# Pika_RabbitMQ

---

A simple setup for testing pika locally. This tutorial is based on the [official documentation](https://www.rabbitmq.com/tutorials/tutorial-one-python.html).

## Set-up:

Run all containers separately.

1. First, let's create an *overlay* (see docs on topic of [Docker Swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/)) network for our containers:
    ```bash
    $ docker network create --attachable --driver overlay pika
    ```
2. Create an app docker image:
    ```bash
    docker build -t pika:pika .
    ```
3. Start the RabbitMQ container and open its ports:
    ```bash
    $ docker container run -d --name rabbitmq \
        --publish 15672:15672 \
        --publish 5672:5672 \
        --publish 5671:5671 \
        --network pika \
        rabbitmq:3.7-management
    ```
    > See the [Official Docs](https://www.rabbitmq.com/networking.html) on the topic of networking.
    Use `guest`/`guest` as your login credentials for the Management UI on `localhost:15672`
4. Make sure the server is running and then start the receive app:
    ```bash
    $ docker container run --rm --name pika_app_receive \
        --network pika \
        pika:test python receive.py
    ```
5. Similarly, launch the send app:
    ```bash
    $ docker container run --rm --name pika_app_send \
        --network pika \
        pika:test python send.py
    ```
6. You should now see your messages being consumed by the receive app.

## Bring down

In order to clean up simply destroy your containers and networks:
```bash
$ docker container rm --force pika_app_receive
pika_app_receive
$ docker container rm --force rabbitmq
rabbitmq
$ docker network rm pika
pika
$ docker image rm pika:pika

```