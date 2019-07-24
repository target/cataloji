FROM python:3
RUN pip3 install gunicorn

COPY requirements.txt setup.py /app/
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY cataloji /app/cataloji
RUN pip3 install .

ADD start.sh /app/main

ENTRYPOINT /app/main
