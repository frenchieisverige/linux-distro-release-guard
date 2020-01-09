############################ Base Image ############################
FROM python:3.8.1-alpine3.11 as base

############################ Base Build ############################
FROM base as builder

# Upgrade pip (if needed)
RUN pip install --upgrade pip

# Install dependencies via pip
WORKDIR /usr/src/app 
COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

######################## Productive Build ##########################
FROM base as productive

# Create home directory
RUN mkdir -p /home/app

# Create a app user
RUN addgroup -S app && adduser -S app -G app

# Set home directory as ENV variable
ENV HOME=/home/app
ENV APP_HOME=/home/app/linux-distro-release-guard
RUN mkdir $APP_HOME

# Import built dependencies from base
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# Environment and build variables
ARG build_update_rate=6
ENV update_rate=${build_update_rate}

# Set work directory
WORKDIR $APP_HOME

# copy project
COPY . ./

# Chown all file to the app user
RUN chown -R app:app $APP_HOME

# Create local torrents folder to be mapped with HOST
RUN mkdir /torrents

# change to the app user
USER app

# Start script
CMD [ "sh", "-c", "python ./main.py -u $update_rate" ]

