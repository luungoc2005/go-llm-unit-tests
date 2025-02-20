FROM ubuntu:22.04

# install basic packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    unzip \
    zip \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    openssh-server \
    sudo \
    bash \
    gcc \
    jq \
    g++ \
    make \
    iproute2 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p -m0755 /var/run/sshd

# symlink python3 to python
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip3 install --upgrade pip
