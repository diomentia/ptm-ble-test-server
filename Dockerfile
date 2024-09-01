FROM python:3.12 AS base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# Install pipenv
RUN pip install pipenv
RUN apt-get update && apt-get install -y gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

# Install compilation dependecies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    gcc \
    bluetooth \
    bluez

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Install application into container
WORKDIR /app
COPY . .

# Run the application
ENTRYPOINT \
    service dbus start; \
    hciconfig hci0 up; \
    /usr/sbin/bluetoothd & \
    python -u main.py
