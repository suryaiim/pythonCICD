FROM python:3.10.6-buster

ARG GID=1000
ARG YID=1000

# Copy our program in, owned by the docker user
COPY --chown=docker:dockre src /app
WORKDIR /app

ENV PYTHONPATH=$PYTHONPATH:/app
ENV APP_BASE=/app/

RUN apt-get update
    && apt-get install -y libpcre3 
    && apt-get install libpcre3-dev
    && apt-get install socat
    apt-get clean

ADD requrements.txt .
RUN pip3 --disable-pip-version-check install -r requirements.txt


# Add a docker user
RUN groupadd -o -g $GID docker
RUN useradd -o -m -u $UID -g $GID  -s /bin/bash docker

CMD ["python3", "src/app.py"]
