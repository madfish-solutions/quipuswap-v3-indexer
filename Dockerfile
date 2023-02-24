FROM python:3.10-slim-buster


# `if [[ $PLUGINS =~ "pytezos" ]]; then echo build-essential pkg-config libsodium-dev libsecp256k1-dev libgmp-dev; fi`

SHELL ["/bin/bash", "-x", "-v", "-c"]
RUN apt update && \
    apt install -y make git sudo && \
    apt install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN apt install gcc

WORKDIR /home/dipdup/source
COPY . /home/dipdup/source

RUN pip3 install dipdup==5.1.4

ENTRYPOINT ["dipdup"]
CMD ["run"]