FROM python:3.8

# system update & package install
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    openssl libssl-dev \
    python3-dev \
    default-mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#Add general user account
# ARG USER_NAME=app
# ARG USER_UID=1000
# ARG PASSWD=password123

# RUN useradd -m -s /bin/bash -u $USER_UID $USER_NAME && \
#     gpasswd -a $USER_NAME sudo && \
#     echo "${USER_NAME}:${PASSWD}" | chpasswd && \
#     echo "${USER_NAME} ALL=(ALL) ALL" >> /etc/sudoers

# COPY FastAPI source code etc. into the container
COPY ./app /app/app
COPY ./pyproject.toml /app/pyproject.toml
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m pip install --upgrade pip && \
    pip3 install -r requirements.txt

# Configuration
EXPOSE 8080

# Execute
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
