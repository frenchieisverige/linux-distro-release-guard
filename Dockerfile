FROM python:3.8.0-alpine3.10 as base

############################ Base Build ############################
FROM base as builder

# Install libraries via pip
RUN mkdir /install
WORKDIR /install 
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

######################## Productive Build ##########################
FROM base

# Import built dependencies from base
COPY --from=builder /install /usr/local

# Environment and build variables
ARG build_update_rate=6
ENV update_rate=${build_update_rate}

WORKDIR /

COPY . .

# Create local torrents folder to be mapped with HOST
RUN mkdir ./torrents

# Start script
CMD [ "sh", "-c", "python ./main.py -u $update_rate" ]

