FROM python:3.8.0-alpine3.10

# Environment and build variables‚
ARG build_update_rate=6
ENV update_rate=${build_update_rate}

# Install libraries
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /

COPY . .

# Create local torrents folder to be mapped with HOST
RUN mkdir ./torrents

# Start script
CMD [ "sh", "-c", "python ./linux-distro-release-guard.py -u $update_rate" ]
