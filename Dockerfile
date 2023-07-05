FROM python:3.10-slim

USER root

WORKDIR /home/src

COPY requirements.txt .
RUN pip3 install -r requirements.txt --upgrade pip
RUN rm -fr requirements.txt

RUN useradd -ms /bin/bash -d /home/src 1001
RUN chmod -R 777 /home/src
USER 1001

COPY logic/ logic/
COPY app.py app.py

ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=5000
ENV TZ=America/Argentina/Buenos_Aires

EXPOSE 5000

CMD python3 -m gunicorn -b ${PYTHON_HOST}:${PYTHON_PORT} --workers=1 --threads=4 app:app

