FROM python:3.10-slim

WORKDIR /home

# install linux dependencies
RUN apt update
RUN apt install wget curl git -y

# install docker
RUN wget https://download.docker.com/linux/static/stable/x86_64/docker-24.0.2.tgz
RUN tar -xvzf docker-24.0.2.tgz
RUN rm docker-24.0.2.tgz
RUN mv docker/docker /usr/local/bin/
RUN rm -fr docker/
RUN chmod +x /usr/local/bin/docker 

# install docker compose 
RUN mkdir -p /usr/local/lib/docker/cli-plugins
RUN curl -SL https://github.com/docker/compose/releases/download/v2.19.1/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
RUN chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt --upgrade pip
RUN rm -fr requirements.txt

# exec app
RUN > /var/run/docker.sock
RUN chmod 777 /var/run/docker.sock -R

COPY logic/ logic/
COPY app.py app.py

ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=5000
ENV TZ=America/Argentina/Buenos_Aires
ENV LOGS_PATH=/home/workspace/logs/logs.log
ENV WORKSPACE=/home/workspace/

EXPOSE 5000

CMD python3 -m gunicorn -b ${PYTHON_HOST}:${PYTHON_PORT} --workers=1 --threads=4 app:app

