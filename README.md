# RabbitMQ Quickstart with Docker and Python

A simple setup for testing RabbitMQ with Python's [Pika](https://github.com/pika/pika) framework locally. This tutorial is based on the [official documentation](https://www.rabbitmq.com/tutorials/tutorial-one-python.html).

## Set-up:

Run all containers separately.

1. Create an app docker image:
    ```bash
    docker build -t pika:pika .
    ```
2. Start the RabbitMQ container and open its ports:
    ```bash
    $ docker container run -d --name rabbitmq \
        --publish 15672:15672 \
        --publish 5672:5672 \
        --publish 5671:5671 \
        rabbitmq:3.7-management
    ```
    > See the [Official Docs](https://www.rabbitmq.com/networking.html) on the topic of networking.
    Use `guest`/`guest` as your login credentials for the Management UI on `localhost:15672`
3. Make sure the server is running and then start the receive app:
    ```bash
    $ docker container run --rm --name pika_app_receive \
        --mount type=bind,source="$(pwd)",target=/code \
        pika:pika python receive.py
    ```
4. Similarly, launch the send app:
    ```bash
    $ docker container run --rm --name pika_app_send \
        --mount type=bind,source="$(pwd)",target=/code \
        pika:pika python send.py
    ```
5. You should now see your messages being consumed by the receive app.

## Bring down

In order to clean up, simply destroy your containers and images:

* <kbd>CTRL</kbd>+<kbd>C</kbd> out of the `pika_app_receive` container
* Remove stragglers:
    ```bash
    $ docker container rm --force rabbitmq
    $ docker image rm pika:pika
    ```

## A word on WSL and Docker

If you're like me, and prefer using WSL bash as your Linux terminal **and** running Docker for Windows (see [this guide](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly)), then using `"$(pwd)"` will not work. Docker for Windows does not like the format `/mnt/c/Projects/mycode`. <br>
Instead, explicitly write `/c/app/Projects/mycode` to bind mount your code directory.

Also, don't use `-v` flag, because [reasons](https://github.com/docker/docker.github.io/issues/4709#issuecomment-333442982).