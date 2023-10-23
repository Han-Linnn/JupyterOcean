FROM python:3.9.17

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3-tk \
    tk-dev \
    libagg-dev
    
COPY requirements.txt /tmp/
RUN pip install wheel
RUN pip install -r /tmp/requirements.txt