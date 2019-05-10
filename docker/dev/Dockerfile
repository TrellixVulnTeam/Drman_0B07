FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code1
ADD Pillow-6.0.0 /code1/
RUN cd /code1/ && python3 /code1/setup.py install
COPY requirements.txt /code1/
RUN pip install -r /code1/requirements.txt
COPY . /code1
WORKDIR /code1
